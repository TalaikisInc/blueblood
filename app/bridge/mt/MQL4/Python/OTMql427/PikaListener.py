# -*-mode: python; py-indent-offset: 4; indent-tabs-mode: nil; encoding: utf-8-dos; coding: utf-8 -*-

"""
This module can be run from the command line to test RabbitMQ
by listening to the broker for messages sent by a speaker
such as PikaChart.py. For example, to see bars and timer topics do:
  python PikaListener.py -v 4 'bar.#' 'timer.#'
The known topics are: bar tick timer retval

Give  --help to see the options.
"""

# We will only have one Pika Connection for any given process, so
# we assign the connection object to the module variable oCONNECTION.
oCONNECTION = None

import sys
import logging
import time

from OTMql427.SimpleFormat import lKNOWN_TOPICS

if True:
    eCALLME_IMPORT_ERROR = "PikaCallme disabled "
    PikaCallme = None

from OTMql427.OTLibLog import vError, vWarn, vInfo, vDebug, vTrace
oLOG = logging


class PikaMixin(object):
    iDeliveryMode = 1 # (non-persisted)
    sContentType = 'text/plain'

    def __init__(self, sChartId, **dParams):
        import pika
        self.oSpeakerChannel = None
        self.oListenerChannel = None
        self.oListenerThread = None
        self.oListenerServer = None
        self.sChartId = sChartId
        self.iSubPubPort = dParams.get('iSubPubPort', 5672)
        self.iReqRepPort = dParams.get('iReqRepPort', 5672)
        self.sHostAddress = dParams.get('sHostAddress', '127.0.0.1')
        # I think really this should be program PID specific
        # I think we want one exchange per terminal process
        self.sExchangeName = dParams.get('sExchangeName', 'Mt4')
        self.sUsername = dParams.get('sUsername', 'guest')
        self.sPassword = dParams.get('sPassword', 'guest')
        # I think really this should be Mt4 specific - for permissions
        self.sVirtualHost = dParams.get('sVirtualHost', '/')
        self.iDebugLevel = dParams.get('iDebugLevel', 4)

        self.oCredentials = pika.PlainCredentials(self.sUsername, self.sPassword)
        #? channel_max heartbeat_interval connection_attempts socket_timeout
        self.oParameters = pika.ConnectionParameters(credentials=self.oCredentials,
                                                     host=self.sHostAddress,
                                                     virtual_host=self.sVirtualHost)
        self.oProperties = pika.BasicProperties(content_type=self.sContentType,
                                                delivery_mode=self.iDeliveryMode)
        self.oConnection = None

    def oCreateConnection(self):
        import pika
        global oCONNECTION
        if not self.oConnection:
            try:
                oConnection = pika.BlockingConnection(self.oParameters)
                assert oConnection, "oCreateConnection: no oConnection created"
                self.oConnection = oConnection
                oCONNECTION = oConnection
                vDebug("Created connection " +str(id(oConnection)))
            except Exception as e:
                #     raise exceptions.ProbableAuthenticationError
                oLOG.exception("Error in oCreateConnection " + str(e))
                raise

        return self.oConnection

    def eBindBlockingSpeaker(self):
        """
        We are going to use our Speaker channel as a broadcast
        channel for ticks, so we will set it up as a "topic".
        """
        if self.oSpeakerChannel is None:
            self.oCreateConnection()
            oChannel = self.oConnection.channel()

            oChannel.exchange_declare(exchange=self.sExchangeName,
                                      passive=False,
                                      # auto_delete=True,
                                      type='topic')

            time.sleep(0.1)
            self.oSpeakerChannel = oChannel
            vDebug("Bound speaker channel " +str(id(oChannel)))

    def eBindBlockingListener(self, sQueueName, lBindingKeys=None):
        """
        """
        if self.oListenerChannel is None:
            if lBindingKeys is None:
                lBindingKeys = ['#']
            self.oCreateConnection()
            oChannel = self.oConnection.channel()

            oChannel.exchange_declare(exchange=self.sExchangeName,
                                      passive=False,
                                      # auto_delete=True,
                                      type='topic')
            # oResult = oChannel.queue_declare(exclusive=True)
            # self.oListenerQueueName = oResult.method.queue
            # I don't think we want exclusive here:
            # we could have more than one listener,
            # and we could have one listening for retvals...
            oResult = oChannel.queue_declare(queue=sQueueName,
                                             exclusive=False)
            self.oListenerQueueName = sQueueName
            for sBindingKey in lBindingKeys:
                oChannel.queue_bind(exchange=self.sExchangeName,
                                    queue=sQueueName,
                                    routing_key=sBindingKey,
                                    )
            time.sleep(0.1)
            self.oListenerChannel = oChannel
            vDebug("Bound listener channel " +str(id(oChannel)))

    def eReturnOnSpeaker(self, sType, sMess, sOrigin):
        """
        """
        if sType not in lKNOWN_TOPICS:
            sRetval = "eReturnOnSpeaker: oSpeakerChannel unhandled topic " +sMess
            vError(sRetval)
            return sRetval

        assert sOrigin, "eReturnOnSpeaker: oSpeakerChannel empty sOrigin"
        lOrigin = sOrigin.split("|")
        assert lOrigin, "eReturnOnSpeaker: oSpeakerChannel empty lOrigin"
        # 'json' was in here
        assert lOrigin[0] in ['eval', 'cmd', 'exec'], \
            "eReturnOnSpeaker: oSpeakerChannel not cmd " +sOrigin
        # This message is a reply in a cmd
        sMark = lOrigin[3]
        assert sMark, "eReturnOnSpeaker: lOrigin[3] is null: " +repr(lOrigin)
        lMess = sMess.split("|")
        assert lMess[0] == 'retval', \
            "eReturnOnSpeaker: lMess[0] should be retval: " +repr(lMess)
        # these now should be equal
        lMess[3] = sMark
        # Replace the mark in the reply with the mark in the cmd
        sMess = '|'.join(lMess)

        return self.eSendOnSpeaker(sType, sMess)

    def eSendOnSpeaker(self, sType, sMess):
        if sType not in lKNOWN_TOPICS:
            sRetval = "eSendOnSpeaker: oSpeakerChannel unhandled topic " +sMess
            vError(sRetval)
            return sRetval
        if self.oSpeakerChannel is None:
            self.eBindBlockingSpeaker()

        assert self.oSpeakerChannel, "eSendOnSpeaker: oSpeakerChannel is null"
        assert self.oConnection, "eSendOnSpeaker: oConnection is null"

        # we will break the sChartId up into dots from the underscores
        # That way the end consumer can look at the feed selectively
        sPublishingKey = sType + '.' + self.sChartId.replace('_', '.')

        self.oSpeakerChannel.basic_publish(exchange=self.sExchangeName,
                                           routing_key=sPublishingKey,
                                           body=sMess,
                                           mandatory=False, immediate=False,
                                           properties=self.oProperties)
        vDebug("eSendOnSpeaker: sent " + sMess)
        return ""

    def vPikaCallbackOnListener(self, oChannel, oMethod, oProperties, lBody):
        # dir(oProperties) = [app_id', 'cluster_id', 'content_encoding', 'content_type', 'correlation_id', 'decode', 'delivery_mode', 'encode', 'expiration', 'headers', 'message_id', 'priority', 'reply_to', 'timestamp', 'type', 'user_id']
        sMess = "vPikaCallbackOnListener: %r" % (lBody, )
        print "INFO: " +sMess
        oChannel.basic_ack(delivery_tag=oMethod.delivery_tag)

    def vPikaRecvOnListener(self, sQueueName, lBindingKeys):
        if self.oListenerChannel is None:
            self.eBindBlockingListener(sQueueName, lBindingKeys)
        assert self.oListenerChannel, "vPikaRecvOnListener: oListenerChannel is null"
        #FixMe: does this block? no
        # http://www.rabbitmq.com/amqp-0-9-1-reference.html#basic.consume
        # no-wait no-wait
        # not in pika.channel.Channel.basic_consume
        self.oListenerChannel.basic_consume(self.vPikaCallbackOnListener,
                                            queue=self.oListenerQueueName,
                                            # exclusive=True,
                                            )

    def bCloseConnectionSockets(self, oIgnored=None):
        import pika
        global oCONNECTION

        # might be called during a broken __init__
        if not hasattr(self, 'oListenerChannel'): return False

        try:
            if self.oListenerChannel:
                # we dont want to purge the queue because we are just a listener
                # blocking_connection.py", line 89, in ready...    self.poll_timeout)
                # throws a select.error: (10004, 'Windows Error 0x2714')
                # self.oListenerChannel.queue_purge(queue=self.oListenerQueueName,
                #                                  nowait=True)
                # TypeError: queue_delete() got an unexpected keyword argument 'callback'
                self.oListenerChannel.queue_delete(queue=self.oListenerQueueName,
                                                   nowait=True)

            if self.oListenerThread:
                self.oListenerThread.stop()
                self.oListenerThread.join()
                self.oListenerThread = None
            elif self.oListenerServer:
                self.oListenerServer.disconnect()
                self.oListenerServer = None

            if self.iDebugLevel >= 1:
                print "DEBUG: destroying the connection"
            sys.stdout.flush()
            sys.stderr.flush()
            if self.oConnection:
                self.oConnection.close()
            if self.oListenerChannel:
                self.oListenerChannel = None
            if self.oSpeakerChannel:
                self.oSpeakerChannel = None
            oCONNECTION = None
        except (KeyboardInterrupt, pika.exceptions.ConsumerCancelled,):
            pass

        time.sleep(0.1)
        return True

def iMain():
    import pika
    from PikaArguments import oParseOptions

    sUsage = __doc__.strip()
    oArgParser = oParseOptions(sUsage)
    oArgParser.add_argument('lArgs', action="store",
                            nargs="*",
                            help="the topics to subscribe to")
    oOptions = oArgParser.parse_args()
    lArgs = oOptions.lArgs

    # FixMe: if no arguments, run a REPL loop dispatching commands
    assert lArgs, "command line arguments required"

    oChart = None
    try:
        if oOptions.iDebugLevel >= 4:
            print "INFO: Listening with binding keys: " +" ".join(lArgs)
        oChart = PikaMixin('oUSDUSD_0_PIKA_0', **oOptions.__dict__)
        oChart.eBindBlockingListener(oOptions.sQueueName, lArgs)

        i = 0
        while i < 5:
            i += 1
            if oOptions.iDebugLevel >= 4:
                print "DEBUG: Listening: " +str(i)
            try:
                #raises:  pika.exceptions.ConnectionClosed
                oChart.vPikaRecvOnListener('listen-for-ticks', lArgs)
                break
            except Exception as e:
                print "WARN: vPikaRecvOnListener " +str(e), i
                continue
        i = 0
        while True:
            i += 1
            try:
                # oChart.oListenerChannel.start_consuming()
                oChart.oConnection.process_data_events()
            except  pika.exceptions.ConnectionClosed:
                print "WARN: ConnectionClosed process_data_events" +str(i)
                time.sleep(1)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print "ERROR: " +str(e)

    try:
        if oChart:
            print "DEBUG: Waiting for message queues to flush..."
            oChart.bCloseConnectionSockets(oOptions)
            time.sleep(1.0)
    except:
        pass

if __name__ == '__main__':
    iMain()
