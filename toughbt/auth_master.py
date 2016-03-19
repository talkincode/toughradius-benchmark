#!/usr/bin/env python
# -*- coding: utf-8 -*-
from txzmq import ZmqEndpoint, ZmqFactory, ZmqPushConnection, ZmqPullConnection
from twisted.internet import reactor
from twisted.python import log
import argparse,sys,os
from txradius import message
from txradius.radius import dictionary,packet
import platform
import itertools
import random
import time

class AuthStatCounter:

    def __init__(self, tparams):
        self.tparams = tparams
        self.starttime = time.time()
        self.requests = 0
        self.replys = 0
        self.accepts = 0
        self.rejects = 0
        self.errors = 0
        self.max_per = 0
        self.max_per_cast = 0
        self.max_time_per = 0
        self.min_time_per = 0
        self.lasttime = self.starttime  
        self.stat_time = self.starttime
        self.stat_num = 0

    def is_done(self):
        return self.requests>0  and self.requests == self.replys

    def process(self,msg):
        self.lasttime = time.time()
        if msg in ('requests','replys','accepts','rejects','errors'):
            setattr(self,msg,getattr(self,msg)+1)
        else:
            print msg

    def get_result(self):
        result = []
        _sectimes = self.lasttime - self.stat_time
        if _sectimes == 0:
            _sectimes = 0.000001

        self.stat_num_old = self.stat_num
        self.stat_num = self.replys
        self.stat_time = self.lasttime
        _sum_nums = self.stat_num - self.stat_num_old
        _percount = _sum_nums /(_sectimes < 0 and 0 or _sectimes)

        _time_per = 0
        if _sum_nums > 0:
            _time_per = (_sectimes/_sum_nums) * 1000

        if self.max_time_per < _time_per:
            self.max_time_per = _time_per
        if self.min_time_per > _time_per or self.min_time_per == 0:
            self.min_time_per = _time_per

        if self.max_per < _percount:
            self.max_per = _percount
            self.max_per_cast = _sectimes
    
        result.append("\n ------------------ radius auth benchmark statistics result ----------------------")
        result.append(" - ")
        result.append(" - Benchmark params")
        result.append(" - ")
        for m in self.tparams:
            result.append(m)
        result.append(" - ")
        result.append(" - Time data statistics")
        result.append(" - ")
        result.append(" - Current stat datetime             :  %s"% time.ctime())
        result.append(" - Current sent request              :  %s"% self.requests)
        result.append(" - Current received response         :  %s"% self.replys)
        result.append(" - Current accepts response          :  %s"% self.accepts)
        result.append(" - Current rejects response          :  %s"% self.rejects)
        result.append(" - Current error response            :  %s"% self.errors)
        result.append(" - Current requests per second       :  %s, stat base %s sec"%(_percount,_sectimes))
        result.append(" - Current max requests per second   :  %s, stat base %s sec"%(self.max_per,self.max_per_cast))
        result.append(" - Current time per request          :  %s ms"%(_time_per))
        result.append(" - Current min time per request      :  %s ms"%(self.min_time_per))
        result.append(" - Current max time per request      :  %s ms"%(self.max_time_per))
        result.append(" - Current Cast total seconds        :  %s sec"%(self.lasttime-self.starttime))
        result.append(" ---------------------------------------------------------------------------------\n")
        return result

class BenchmarkMaster:

    def __init__(self,server,port,secret,requests,concurrency,username,password,
        verb=False,timeout=30,forknum=1,interval=2,rate=1000):
        self.interval = interval
        tparams = [
            ' - Client platform                   :  %s, %s'% (platform.platform(),platform.machine()),
            ' - Python implement, version         :  %s, %s'% (platform.python_implementation(), platform.python_version()),
            ' - Radius server  address            :  %s'% server,
            ' - Radius Server auth port           :  %s'% port,
            ' - Raduius share secret              :  %s'% secret,
            ' - Auth Request total                :  %s'% requests,
            ' - Concurrency level                 :  %s'% concurrency,
            ' - Worker Process num                :  %s'% forknum,
            ' - All Requests timeout              :  %s sec'% timeout,
            ' - Stat data interval                :  %s sec'% interval,
            ' - Send request rate                 :  %s/sec'% rate,
        ]
        self.stat_counter = AuthStatCounter(tparams)
        self.puller = ZmqPullConnection(ZmqFactory(), ZmqEndpoint('bind', 'ipc:///tmp/toughbt-message'))
        self.puller.onPull = self.do_stat
        # log.msg("init BenchmarkMaster puller : %s " % (self.puller))
        
        reactor.callLater(interval,self.chk_task)
        reactor.callLater(timeout,reactor.stop)

    def do_stat(self,message):
        try:
            if message[0].startswith('logger:'):
                self.stat_counter.process(message[0])
            else:
                for m in message[0].split(','):
                    self.stat_counter.process(m)
        except:
            import traceback
            traceback.print_exc()
        
    def chk_task(self):
        print "\n".join(self.stat_counter.get_result())
        if self.stat_counter.is_done():
            print 'benchmark done!'
            reactor.callLater(1.0,reactor.stop)
        else:
            reactor.callLater(self.interval,self.chk_task)

    



















