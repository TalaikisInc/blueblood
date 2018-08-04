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

import inspect
import itertools
import functools
import json
import math
import os
import random
import threading
import time

from collections import deque, defaultdict
from copy import copy
from datetime import date, datetime, timedelta
from functools import partial

import pyiqfeed as iq
import pandas
import pytz

import backtrader as bt
from backtrader import Position
from backtrader.metabase import MetaParams
from backtrader.utils.py3 import queue, with_metaclass, urlopen
from backtrader.utils import AutoDict


def to_datetime(dtime64, msecs, tz=pytz.utc):
    """Convert data and time since midnight to datetime.datetime"""
    assert msecs >= 0
    assert msecs <= 86400000000
    microsecond = msecs % 1000000
    secs_since_midnight = math.floor(msecs / 1000000.0)
    hour = math.floor(secs_since_midnight / 3600)
    minute = math.floor((secs_since_midnight - (hour * 3600)) / 60)
    second = secs_since_midnight - (hour * 3600) - (minute * 60)
    date = dtime64.astype(datetime)
    dt = datetime(year=date.year,
                  month=date.month,
                  day=date.day,
                  hour=int(hour),
                  minute=int(minute),
                  second=int(second),
                  microsecond=int(microsecond))
    return tz.localize(dt)

class IQFeedLevel1QuoteListener(iq.VerboseIQFeedListener):
    def __init__(self, name, store):
        iq.VerboseIQFeedListener.__init__(self, name)
        self.store = store

    def process_update(self, update):
        for symbol, tick, mopen in update:
            self.store.marketopen[symbol] = mopen

    process_summary = process_update

    def empty(self, param):
        pass

    process_ip_addresses_used = process_auth_key = process_customer_info = \
        process_timestamp = process_fundamentals = empty

class IQFeedBarListener(iq.VerboseBarListener):
    def __init__(self, name, queue, store):
        iq.VerboseBarListener.__init__(self, name)
        self.queue = queue
        self.store = store

    def process_history_bar(self, bar_data):
        pass

    def process_live_bar(self, bar_data):
        self.store.last_activity = datetime.now()
        for bar in bar_data:
            _ticker, _date, _time, _open, _high, _low, _close, _volume, _openinterest, _ = bar
            #print(">>> process_live_bar:", to_datetime(_date, _time, pytz.timezone('US/Eastern')), _ticker, self.queue[_ticker])
            if self.store.marketopen[_ticker]:
                self.queue[_ticker].put({'datetime': to_datetime(_date, _time, pytz.timezone('US/Eastern')),
                                         'open': _open,
                                         'high': _high,
                                         'low': _low,
                                         'close': _close,
                                         'volume': _volume,
                                         'openinterest': _openinterest})

class MetaSingleton(MetaParams):
    '''Metaclass to make a metaclassed class a singleton'''
    def __init__(cls, name, bases, dct):
        super(MetaSingleton, cls).__init__(name, bases, dct)
        cls._singleton = None

    def __call__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = (
                super(MetaSingleton, cls).__call__(*args, **kwargs))

        return cls._singleton

class IQFeedStore(with_metaclass(MetaSingleton, object)):
    '''Singleton class wrapping IQFeed connections.
    The parameters can also be specified in the classes which use this store,
    like ``IQFeedData``
    Params:
      - ``notifyall`` (default: ``False``)
        If ``False`` only ``error`` messages will be sent to the
        ``notify_store`` methods of ``Cerebro`` and ``Strategy``.
        If ``True``, each and every message received from IQFeed will be notified
      - ``debug`` (default: ``False``)
        Print all messages received from IQFeed to standard output
    '''
    BrokerCls = None  # broker class will autoregister
    DataCls = None  # data class will auto register

    params = (
        ('fields', sorted(iq.QuoteConn.quote_msg_map)),
        ('notifyall', False),
        ('debug', False),
        ('ping_interval', 5),
        ('timeout', 120),
        ('reconnect', False),
    )

    def getdata(cls, *args, **kwargs):
        '''Returns ``DataCls`` with args, kwargs'''
        return cls.DataCls(*args, **kwargs)

    @classmethod
    def getbroker(cls, *args, **kwargs):
        '''Returns broker with *args, **kwargs from registered ``BrokerCls``'''
        return cls.BrokerCls(*args, **kwargs)

    def __init__(self):
        super(IQFeedStore, self).__init__()

        self.notifs = deque()  # store notifications for cerebro

        self._env = None  # reference to cerebro for general notifications
        self.broker = None  # broker instance
        self.datas = list()  # datas that have registered over start

        self.queues = defaultdict(partial(defaultdict, queue.Queue)) # message queues
        self.threads = {}  # IQFeed connection threads

        self.stopped = False
        self.last_activity = datetime.now() # datetime of the latest received message
        self.marketopen = {} # 'Market Open' flag from IQFeed

    def run_forever(self, timeframe):
        """Start listening to IQFeed bars for the specified time frame."""
        quote_conn = iq.QuoteConn(name="IQFeed Quote Conn %s" % bt.TimeFrame.getname(timeframe))
        quote_listener = IQFeedLevel1QuoteListener("IQFeed Level 1 Quote Listener %s" % \
                                                   bt.TimeFrame.getname(timeframe), self)
        quote_conn.add_listener(quote_listener)

        bar_conn = iq.BarConn(name="IQFeed Bar Conn %s" % bt.TimeFrame.getname(timeframe))
        bar_listener = IQFeedBarListener("IQFeed Bar listener %s" % bt.TimeFrame.getname(timeframe),
                                         self.queues[timeframe], self)
        bar_conn.add_listener(bar_listener)

        watched = []
        with iq.ConnConnector([bar_conn, quote_conn]) as connector:
            quote_conn.select_update_fieldnames(['Symbol', 'Tick', 'Market Open'])
            while not self.stopped:
                for data in self.datas:
                    if data.p.timeframe == timeframe and id(data) not in watched:
                        interval_type = 't' if data.p.timeframe == bt.TimeFrame.Ticks else 's'
                        interval_len = {bt.TimeFrame.Ticks: 1,
                                        bt.TimeFrame.Seconds: 1,
                                        bt.TimeFrame.Minutes: 60}.get(data.p.timeframe)
                        bar_conn.watch(symbol=data.p.dataname,
                                       interval_len=interval_len * data.p.compression,
                                       interval_type=interval_type,
                                       bgn_bars=None,
                                       lookback_days=1,
                                       lookback_bars=None,
                                       bgn_flt=data.p.sessionstart,
                                       end_flt=data.p.sessionend,
                                       update=0)
                        watched.append(id(data))
                        quote_conn.watch(data.p.dataname)
                time.sleep(0.1)

        for data in self.datas:
            quote_conn.unwatch(data.p.dataname)
            if data.p.timeframe == timeframe:
                bar_conn.unwatch(data.p.dataname)

        bar_conn.remove_listener(bar_listener)
        quote_conn.remove_listener(quote_listener)

    def start(self, data=None, broker=None):
        if broker is not None:
            self.broker = broker

        if data is not None:
            self._env = data._env
            self.datas.append(data)

            # start one event loop per time frame
            if not data.p.historical and data.p.timeframe not in self.threads:
                thread = threading.Thread(target=self.run_forever,
                                          kwargs={'timeframe': data.p.timeframe})
                thread.setDaemon(True)
                self.threads[data.p.timeframe] = thread
                thread.start()

    def put_notification(self, msg, *args, **kwargs):
        self.notifs.append((msg, args, kwargs))

    def get_notifications(self):
        '''Return the pending "store" notifications'''
        self.notifs.append(None)  # put a mark / threads could still append
        return [x for x in iter(self.notifs.popleft, None)]

    def connected(self):
        return datetime.now() - self.last_activity < timedelta(seconds=self.p.timeout)

    def stop(self):
        if not self.stopped:
            self.stopped = True
        for thread in self.threads.values():
            thread.join()
        self.threads = {}

    def get_history(self, dataname, dtbegin, dtend, timeframe, compression):
        q = queue.Queue()
        if timeframe not in (bt.TimeFrame.Ticks, bt.TimeFrame.Seconds, bt.TimeFrame.Minutes,
                             bt.TimeFrame.Days, bt.TimeFrame.Weeks, bt.TimeFrame.Months) or \
           (timeframe in (bt.TimeFrame.Days, bt.TimeFrame.Weeks, bt.TimeFrame.Months) and \
            compression != 1):
            err = "Unsupported timeframe/compression: %s/%s" % \
                  (bt.TimeFrame.getname(timeframe), compression)
            self.put_notification(err, (), {})
            q.put({"error": err})
            return q

        hist_conn = iq.HistoryConn(name="IQFeed Store History")

        cdata = [data for data in self.datas if data._dataname == dataname][0]

        with iq.ConnConnector([hist_conn]) as connector:
            try:
                if timeframe in (bt.TimeFrame.Ticks, bt.TimeFrame.Seconds, bt.TimeFrame.Minutes):
                    interval_type = 't' if timeframe == bt.TimeFrame.Ticks else 's'
                    interval_len = compression * 60 if timeframe == bt.TimeFrame.Minutes else compression
                    bars = hist_conn.request_bars_in_period(ticker=dataname,
                                                            interval_len=interval_len,
                                                            interval_type=interval_type,
                                                            bgn_prd=dtbegin,
                                                            end_prd=dtend,
                                                            bgn_flt=cdata.p.sessionstart,
                                                            end_flt=cdata.p.sessionend,
                                                            ascend=True)
                elif timeframe == bt.TimeFrame.Days:
                    bars = hist_conn.request_daily_data_for_dates(ticker=dataname,
                                                                  bgn_dt=dtbegin,
                                                                  end_dt=dtend,
                                                                  ascend=True)
                elif timeframe == bt.TimeFrame.Weeks:
                    num_weeks = math.ceil((dtend - dtbegin).days / 7.0)
                    bars = hist_conn.request_weekly_data(dataname, num_weeks, ascend=True)
                elif timeframe == bt.TimeFrame.Months:
                    num_months = 12 * dtend.year + dtend.month - 12 * dtbegin.year - dtbegin.month
                    bars = hist_conn.request_monthly_data(dataname, num_months, ascend=True)
            except (iq.NoDataError, iq.UnauthorizedError) as err:
                error = "Unable to get historical data. Error:" % err
                self.put_notification(error, (), {})
                q.put({"error": error})
                return q

        for bar in bars:
            if len(bar) == 7:
                dte, opn, high, low, close, volume, oint = bar
                dte = dte.astype(date)
                dtime = datetime(dte.year, dte.month, dte.day)
            else:
                dt64, tm64, opn, high, low, close, volume, pvolume, oint = bar
                dtime = dt64 + tm64
                dtime = dtime.astype(datetime)

            q.put({'date': cdata.p.tz.localize(dtime),
                   'open': opn, 'high': high, 'low': low, 'close': close,
                   'volume': volume, 'openinterest': oint})

        q.put({})  # end of transmission
        return q
