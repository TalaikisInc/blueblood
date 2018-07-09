# -*-mode: python; py-indent-offset: 4; indent-tabs-mode: nil; encoding: utf-8-dos; coding: utf-8 -*-

"""
A PikaChart object is a simple abstraction to encapsulate a Mt4 chart
that has a RabbitMQ connection on it. There should be only one connection for
the whole application, so it is set as the module variable oCONNECTION.

This module can be run from the command line to test RabbitMQ with a listener
such as OTMql427/PikaListener.py. Give the message you want to publish
as arguments to this script, or --help to see the options.
"""

import sys, logging
import time
import traceback
import pika

oLOG = logging

from Mq4Chart import Mq4Chart, oFindChartByName, lFindAllCharts
from PikaListener import PikaMixin
from Mt4SafeEval import sPySafeEval
from SimpleFormat import lUnFormatMessage

if True:
    ePikaCallme = "PikaCallme disabled "
    PikaCallme = None
else:
    # The callme server is optional and may not be installed.
    # But it might be a whole lot of fun it it works.
    # It has prerequisities: kombu httplib2 amqp
    try:
        import PikaCallme
        ePikaCallme = ""
    except ImportError as e:
        ePikaCallme = "Failed to import PikaCallme: " + str(e)
        PikaCallme = None

class PikaChart(Mq4Chart, PikaMixin):

    iDeliveryMode = 1 # (non-persisted)
    sContentType = 'text/plain'

    def __init__(self, sChartId, **dParams):
        Mq4Chart.__init__(self, sChartId, **dParams)
        PikaMixin.__init__(self, sChartId, **dParams)
        self.sChartId = sChartId
        self.sQueueName = "listen-for-commands"

    def vPikaRecvOnListener(self, sQueueName, lBindingKeys):
        if self.oListenerChannel is None:
            self.eBindBlockingListener(sQueueName, lBindingKeys)
        assert self.oListenerChannel, "vPikaRecvOnListener: oListenerChannel is null"
        #FixMe: does this block?
        # http://www.rabbitmq.com/amqp-0-9-1-reference.html#basic.consume
        # no-wait no-wait
        # not in pika.channel.Channel.basic_consume
        self.oListenerChannel.basic_consume(self.vPikaCallbackOnListener,
                                            queue=self.oListenerQueueName,
                                            exclusive=True,
                                            no_ack=False
        )

    def eHeartBeat(self, iTimeout=0):
        """
        The heartbeat is usually called from the Mt4 OnTimer.
        We push a simple Print exec command onto the queue of things
        for Mt4 to do if there's nothing else happening. This way we get
        a message in the Mt4 Log,  but with a string made in Python.
        """
        if self.oQueue.empty():
            # only push if there is nothing to do
            sTopic = 'exec'
            sMark = "%15.5f" % time.time()
            sInfo = "PY: " +sMark
            sMess = "%s|%s|0|%s|Print|%s" % (sTopic, self.sChartId, sMark, sInfo,)
            self.eMq4PushQueue(sMess)

        # while we are here flush stdout so we can read the log file
        # whilst the program is running
        sys.stdout.flush()
        sys.stderr.flush()

        # now for the hard part - see if there is anything to receive
        # does this block? do we set a timeout?
        if self.oListenerChannel is None:
            # , 'json.#'
            lBindingKeys = ['cmd.#', 'eval.#']
            self.vPikaRecvOnListener(self.sQueueName, lBindingKeys)

        # This is the disabled callme server code
        if iTimeout > 0 and self.oListenerServer:
            # join it and do a little work but dont block for long
            # cant use self.oListenerServer.wait()
            print "DEBUG: listening on server"
            self.oListenerServer.drain_event(iTimeout=iTimeout)

        return ""

    def vPikaDispatchOnListener(self, sBody, oProperties=None):
        #? do we need the oProperties for content-type?
        # 'content_encoding', 'content_type', 'correlation_id', 'decode', 'delivery_mode', 'encode', 'expiration', 'headers', 'message_id', 'priority', 'reply_to', 'timestamp', 'type', 'user_id'

        lArgs = lUnFormatMessage(sBody)
        sMsgType = lArgs[0]
        sChart = lArgs[1]
        sIgnore = lArgs[2] # should be a hash on the payload
        sMark = lArgs[3]
        sVerbMaybe = lArgs[4]
        gPayload = lArgs[4:] # overwritten below

        if sMsgType == 'cmd':
            # FixMe; dispatch to the right chart
            lChartInstances = lFindAllCharts()
            if not lChartInstances:
                # this should never happen
                sys.stdout.write("ERROR: vPikaDispatchOnListener no charts\n")
                self.eMq4PushQueue(sBody)
                return
            if sChart.find('ANY') >= 0:
                #? use self?
                oElt =lChartInstances[0]
                oElt.eMq4PushQueue(sBody)
                return
            if sChart.find('ALL') >= 0:
                for oElt in lChartObjects:
                    oElt.eMq4PushQueue(sBody)
                return

            o = oFindChartByName(sChart)
            if o is not None:
                o.eMq4PushQueue(sBody)
                return

            sys.stdout.write("WARN: vPikaDispatchOnListener unrecognized sBody " +sBody +"\n")
            sys.stdout.flush()

            self.eMq4PushQueue(sBody)
            return

        #? assume eval is on any chart?
        if sMsgType == 'eval':
            # unused
            lRetval = ['retval']
            lRetval += lArgs[1:3]
            sCmd = lArgs[4]
            if len(lArgs) > 5:
                sCmd += '(' +lArgs[5] +')'
            sRetval = sPySafeEval(sCmd)
            if sRetval.find('ERROR:') >= 0:
                lRetval += ['error', sRetval]
            else:
                lRetval += ['string', sRetval]
            sRetval = '|'.join(lRetval)
            # FixMe; dispatch to the right chart
            self.eReturnOnSpeaker('retval', sRetval, sBody)
            return

    def vPikaCallbackOnListener(self, oChannel, oMethod, oProperties, sBody):
        assert sBody, "vPikaCallbackOnListener: no sBody received"
        oChannel.basic_ack(delivery_tag=oMethod.delivery_tag)
        sMess = "vPikaCallbackOnListener Listened: %r" % sBody
        sys.stdout.write("INFO: " +sMess +"\n")
        sys.stdout.flush()
        # we will assume that the sBody
        # is a "|" seperated list of command and arguments
        # FixMe: the sMess must be in the right format
        # FixMe: refactor for multiple charts:
        # we must push to the right chart
        try:
            self.vPikaDispatchOnListener(sBody, oProperties)
        except Exception as e:
            sys.stdout.write("ERROR: " +str(e) +"\n" + \
                             traceback.format_exc(10) +"\n")
            sys.stdout.flush()
            sys.exc_clear()

    # unused
    def eStartCallmeServer(self, sId='Mt4Server'):
        # The callme server is optional and may not be installed
        if not PikaCallme:
            return ePikaCallme
        if self.oListenerServer is None:
            oServer = PikaCallme.Server(server_id=sId)
            # danger - we are running this in the main thread
            # self.oListenerThread = _run_server_thread(oServer)
            oServer.connect()
            oServer.register_function(sPySafeEval, 'sPySafeEval')
            oServer.register_function(self.eMq4PushQueue, 'eMq4PushQueue')
            self.oListenerServer = oServer
            print "DEBUG: started the callme server %d" % id(oServer)

        return ""


def iMain():
    from PikaArguments import oParseOptions

    sUsage = __doc__.strip()
    oArgParser = oParseOptions(sUsage)
    oArgParser.add_argument('lArgs', action="store",
                            nargs="*",
                            help="the message to send (required)")
    oOptions = oArgParser.parse_args()
    lArgs = oOptions.lArgs

    assert lArgs, "Give the command you want to send as arguments to this script"

    sSymbol = 'ANY'
    iPeriod = 0
    sTopic = 'cmd'
    sMark = "%15.5f" % time.time()
    sMsg = "%s|%s|0|%s|%s|str|%s" % (sTopic, sSymbol+str(iPeriod), sMark, '|'.join(lArgs),)

    oChart = None
    try:
        oChart = PikaChart('oANY_0_FFFF_0', **oOptions.__dict__)
        iMax = 1
        i = 0
        print "Sending: %s %d times " % (sMsg, iMax,)
        while i < iMax:
            # send a burst of iMax copies
            oChart.eSendOnSpeaker('cmd', sMsg)
            i += 1
        # print "Waiting for message queues to flush..."
        time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(traceback.format_exc(10))

    try:
        if oChart:
            print "DEBUG: Waiting for message queues to flush..."
            oChart.bCloseConnectionSockets(oOptions)
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    iMain()
