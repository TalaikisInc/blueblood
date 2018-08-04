#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015, 2016, 2017 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from datetime import datetime

import backtrader as bt
from backtrader.feed import DataBase
from backtrader import TimeFrame, date2num, num2date
from backtrader.utils.py3 import (integer_types, queue, string_types,
                                  with_metaclass)
from backtrader.metabase import MetaParams
from backtrader.stores import IQFeedStore

class MetaIQFeed(DataBase.__class__):
    def __init__(cls, name, bases, dct):
        '''Class has already been created ... register'''
        # Initialize the class
        super(MetaIQFeed, cls).__init__(name, bases, dct)

        # Register with the store
        IQFeedStore.DataCls = cls


class IQFeed(with_metaclass(MetaIQFeed, DataBase)):
    '''IQFeed Data Feed.
    Params:
      - ``historical`` (default: ``False``)
        If set to ``True`` the data feed will stop after doing the first
        download of data.
        The standard data feed parameters ``fromdate`` and ``todate`` will be
        used as reference.
      - ``qcheck`` (default: ``0.5``)
        Time in seconds to wake up if no data is received to give a chance to
        resample/replay packets properly and pass notifications up the chain
      - ``backfill_start`` (default: ``True``)
        Perform backfilling at the start. The maximum possible historical data
        will be fetched in a single request.
      - ``backfill`` (default: ``True``)
        Perform backfilling after a disconnection/reconnection cycle. The gap
        duration will be used to download the smallest possible amount of data
      - ``backfill_from`` (default: ``None``)
        An additional data source can be passed to do an initial layer of
        backfilling. Once the data source is depleted and if requested,
        backfilling from Gemini will take place. This is ideally meant to
        backfill from already stored sources like a file on disk, but not
        limited to.
      - ``reconnect`` (default: ``True``)
        Reconnect when network connection is down
      - ``reconnections`` (default: ``-1``)
        Number of times to attempt reconnections: ``-1`` means forever
      - ``reconntimeout`` (default: ``5.0``)
        Time in seconds to wait in between reconnection attemps
    '''
    params = (
        ('historical', False),  # only historical download
        ('qcheck', 0.5),  # timeout in seconds (float) to check for events
        ('backfill_start', False),  # do backfilling at the start
        ('backfill', True),  # do backfilling when reconnecting
        ('backfill_from', None),  # additional data source to do backfill from
        ('reconnect', True),
        ('reconnections', -1),  # forever
        ('reconntimeout', 5.0),
        ('debug', False), # debug output
    )

    # States for the Finite State Machine in _load
    _ST_FROM, _ST_START, _ST_LIVE, _ST_HISTORBACK, _ST_OVER = range(5)

    def islive(self):
        '''Returns ``True`` to notify ``Cerebro`` that preloading and runonce
        should be deactivated'''
        return True

    def __init__(self, **kwargs):
        self.store = IQFeedStore(**kwargs)

    def setenvironment(self, env):
        '''Receives an environment (cerebro) and passes it over to the store it
        belongs to'''
        super(IQFeed, self).setenvironment(env)
        env.addstore(self.store)

    def start(self):
        '''Starts the IQFeed connection'''
        super(IQFeed, self).start()

        # Kickstart store and get queue to wait on
        self._statelivereconn = False  # if reconnecting in live state
        self._storedmsg = dict()       # keep pending live message (under None)
        self.qlive = self.store.queues[self.p.timeframe][self.p.dataname]
        self.qhist = None
        self._state = self._ST_OVER

        # Kickstart store
        self.store.start(data=self)

        self.put_notification(self.CONNECTED)

        if self.p.backfill_from is not None:
            self._state = self._ST_FROM
            self.p.backfill_from._start()
        else:
            self._start_finish()
            self._state = self._ST_START  # initial state for _load
            self._st_start()

        self._reconns = 0

    def _st_start(self, instart=True, tmout=None):
        if self.fromdate != float("-inf"):
            self.put_notification(self.DELAYED)

            dtend = None
            if self.todate < float('inf'):
                dtend = num2date(self.todate)

            dtbegin = None
            if self.fromdate > float('-inf'):
                dtbegin = num2date(self.fromdate)

            self.qhist = self.store.get_history(self.p.dataname, dtbegin, dtend,
                                                self._timeframe, self._compression)

            self._state = self._ST_HISTORBACK
            if self.p.historical:
                return True

        else:
            self._state = self._ST_LIVE

        if instart:
            self._statelivereconn = self.p.backfill_start
            self._reconns = self.p.reconnections
        else:
            self._statelivereconn = self.p.backfill

        if self._statelivereconn:
            self.put_notification(self.DELAYED)

        return True

    def stop(self):
        '''Stops and tells the store to stop'''
        super(IQFeed, self).stop()
        self.store.stop()

    def haslivedata(self):
        return True

    def _load(self):
        if self._state == self._ST_OVER:
            return False

        while True:
            if self._state == self._ST_LIVE:
                try:
                    msg = (self._storedmsg.pop(None, None) or
                           self.qlive.get(timeout=self._qcheck))
                except queue.Empty:
                    return None  # indicate timeout situation

                if msg is None:  # Conn broken during historical/backfilling
                    self.put_notification(self.CONNBROKEN)
                    # Try to reconnect
                    if not self.p.reconnect or self._reconns == 0:
                        # Can no longer reconnect
                        self.put_notification(self.DISCONNECTED)
                        self._state = self._ST_OVER
                        return False  # failed

                    self._reconns -= 1
                    self._st_start(instart=False, tmout=self.p.reconntimeout)
                    continue

                if not self.store.connected():
                    self.put_notification(self.CONNBROKEN)

                    # Can reconnect
                    self._reconns -= 1
                    self._st_start(instart=False, tmout=self.p.reconntimeout)
                    continue

                self._reconns = self.p.reconnections
                # Process the message according to expected return type
                if not self._statelivereconn:
                    if self._laststatus != self.LIVE:
                        if self.qlive.qsize() <= 1:  # very short live queue
                            self.put_notification(self.LIVE)

                    ret = self._load_bar(msg)
                    if ret:
                        return True

                    # could not load bar ... go and get new one
                    continue

                # Fall through to processing reconnect - try to backfill
                self._storedmsg[None] = msg  # keep the msg

                # else do a backfill
                if self._laststatus != self.DELAYED:
                    self.put_notification(self.DELAYED)

                if len(self) > 1:
                    # len == 1 ... forwarded for the 1st time
                    dtbegin = self.datetime.datetime(-1)
                elif self.fromdate > float('-inf'):
                    dtbegin = num2date(self.fromdate)
                else:  # 1st bar and no begin set
                    # passing None to fetch max possible in 1 request
                    dtbegin = None

                dtend = msg['datetime']
                self.qhist = self.store.get_history(self.p.dataname, dtbegin, dtend,
                                                    self._timeframe, self._compression)

                self._state = self._ST_HISTORBACK
                self._statelivereconn = False  # no longer in live
                continue

            elif self._state == self._ST_HISTORBACK:
                msg = self.qhist.get()
                if msg is None:  # Conn broken during historical/backfilling
                    # Situation not managed. Simply bail out
                    self.put_notification(self.DISCONNECTED)
                    self._state = self._ST_OVER
                    return False  # error management cancelled the queue

                elif 'error' in msg:  # Error
                    self.put_notification(self.DISCONNECTED)
                    self._state = self._ST_OVER
                    return False

                if msg:
                    if self._load_history(msg):
                        return True  # loading worked

                    continue  # not loaded ... date may have been seen
                else:
                    # End of histdata
                    if self.p.historical:  # only historical
                        self.put_notification(self.DISCONNECTED)
                        self._state = self._ST_OVER
                        return False  # end of historical

                # Live is also wished - go for it
                self._state = self._ST_LIVE
                continue

            elif self._state == self._ST_FROM:
                if not self.p.backfill_from.next():
                    # additional data source is consumed
                    self._state = self._ST_START
                    continue

                # copy lines of the same name
                for alias in self.lines.getlinealiases():
                    lsrc = getattr(self.p.backfill_from.lines, alias)
                    ldst = getattr(self.lines, alias)

                    ldst[0] = lsrc[0]

                return True

            elif self._state == self._ST_START:
                if not self._st_start(instart=False):
                    self._state = self._ST_OVER
                    return False

    def _load_bar(self, event):
        dt = date2num(event['datetime'])
        if dt <= self.lines.datetime[-1]:
            return False # cannot deliver earlier than already delivered

        self.lines.datetime[0] = dt

        self.lines.open[0] = event['open']
        self.lines.high[0] = event['high']
        self.lines.low[0] = event['low']
        self.lines.close[0] = event['close']
        self.lines.volume[0] = event['volume']
        self.lines.openinterest[0] = event['openinterest']

        return True

    def _load_history(self, bar):
        dt = date2num(bar['date'])
        if dt <= self.lines.datetime[-1]:
            return False  # time already seen

        self.lines.datetime[0] = dt
        self.lines.open[0] = bar['open']
        self.lines.high[0] = bar['high']
        self.lines.low[0] = bar['low']
        self.lines.close[0] = bar['close']
        self.lines.volume[0] = bar['volume']
        self.lines.openinterest[0] = bar['openinterest']

        return True
