# -*-mode: python; py-indent-offset: 4; indent-tabs-mode: nil; encoding: utf-8-dos; coding: utf-8 -*-

"""
This file declares oParseOptions in a separate file so that the
arguments parsing can be uniform between applications that use it.

"""

from argparse import ArgumentParser

def oParseOptions(sUsage):
    """
    Look at the bottom of PikaListener.py and PikaChart.py for iMain
    functions that use the oParseOptions that is returned here.
    This function returns an ArgumentParser instance, so that you
    can override it before you call it to parse_args.
    """
    oArgParser = ArgumentParser(description=sUsage)
    # rabbit
    oArgParser.add_argument("-a", "--address",
                            action="store",
                            dest="sHostAddress",
                            default="127.0.0.1",
                            help="the TCP address to subscribe on (default 127.0.0.1)")
    oArgParser.add_argument("-o", "--pubport", action="store",
                            dest="iPubPort", type=int, default=5672,
                            help="the TCP port number to publish to (default 5672)")
    oArgParser.add_argument("-u", "--username", action="store",
                            dest="sUsername", default="guest",
                            help="the username for the connection (default guest)")
    oArgParser.add_argument("-p", "--password", action="store",
                            dest="sPassword", default="guest",
                            help="the password for the connection (default guest)")
    oArgParser.add_argument("-e", "--exchange", action="store",
                            dest="sExchangeName", default="Mt4",
                            help="sExchangeName for the connection (default Mt4)")
    oArgParser.add_argument("-P", "--mt4dir", action="store",
                            dest="sMt4Dir", default="",
                            help="directory for the installed Metatrader")
    oArgParser.add_argument("-i", "--virtual", action="store",
                            dest="sVirtualHost", default="/",
                            help="the VirtualHost for the connection (default /)")
    oArgParser.add_argument("-q", "--queue", action="store",
                            dest="sQueueName", default="listen-for-ticks",
                            help="the VirtualHost for the connection (default listen-for-ticks)")
    oArgParser.add_argument("-v", "--verbose", action="store",
                            dest="iDebugLevel", type=int, default=4,
                            help="the verbosity, 0 for silent 4 max (default 4)")
    return oArgParser

