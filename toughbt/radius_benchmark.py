#!/usr/bin/env python
# -*- coding: utf-8 -*-
from toughbt import choosereactor
choosereactor.install_optimal_reactor(True)
from twisted.internet import reactor
from twisted.python import log
import argparse,sys,os
from toughbt import radiusclient
from txradius import message
from txradius.radius import dictionary,packet
import itertools
import random
import time
reactor.suggestThreadPoolSize(60)

class AuthStatCounter:

    def __init__(self):
        self.starttime = time.time()
        self.requests = 0
        self.replys = 0
        self.accepts = 0
        self.rejects = 0
        self.errors = 0
        self.max_per = 0
        self.lasttime = self.starttime  
        self.stat_time = time.time()

    def error(self,err):
        self.errors += 1

    def plus(self,auth_resp):
        if auth_resp.code== packet.AccessReject:
            self.rejects += 1
        if auth_resp.code== packet.AccessAccept:
            self.accepts += 1
        self.replys += 1
        self.lasttime = time.time()

    def get_result(self):
        result = []
        _sectimes = self.lasttime - self.starttime
        if _sectimes <= 0:
            return ''
        _percount = self.replys /(_sectimes < 0 and 0 or _sectimes)
        if self.max_per < _percount:
            self.max_per = _percount
        result.append("\n ###################################################")
        result.append(" # Current datetime                  : %s"% time.ctime())
        result.append(" # Current sender request            : %s"% self.requests)
        result.append(" # Current received response         : %s"% self.replys)
        result.append(" # Current accepts response          : %s"% self.accepts)
        result.append(" # Current rejects response          : %s"% self.rejects)
        result.append(" # Current error sent                : %s"% self.errors)
        result.append(" # Current response num per second   : %s"%_percount)
        result.append(" # Max response num per second       : %s"%self.max_per)
        result.append(" # All request Cast total second     : %s"%(time.time()-self.starttime))
        result.append(" ######################################################\n")
        self.stat_time = self.lasttime
        return result

def random_mac():
    mac = [ 0x52, 0x54, 0x00,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def auth_test(server,port,secret,requests,concurrency,username,password,verb=False,timeout=30):
    stat_counter = AuthStatCounter()
    raddict = dictionary.Dictionary(os.path.join(os.path.dirname(__file__),"dictionary"))
    _clis = []
    for c in range(concurrency):
        _clis.append(radiusclient.RadiusClient(str(secret), raddict, server,port,debug=verb,stat_counter=stat_counter))
    clis = itertools.cycle(_clis)

    

    def chk_task():
        print "\n".join(stat_counter.get_result())
        if stat_counter.replys == requests:
            reactor.callLater(1.0,reactor.stop)
        else:
            reactor.callLater(1.0,chk_task)

    reactor.callLater(2.0,chk_task)

    for i in xrange(requests):
        radcli = next(clis)
        radcli.sendAuth(**{'User-Name' : username,'User-Password':password})


def exit(parser,status, msg=''):
    print (msg)
    parser.print_help()
    sys.exit(1)

def run():
    # log.startLogging(sys.stdout)
    parser = argparse.ArgumentParser()
    parser.add_argument('-auth', '--auth', action='store_true', default=False, dest='auth', 
        help='Run radius auth test')
    parser.add_argument('-acct', '--acct', action='store_true', default=False, dest='acct', 
        help='Run radius acct test')
    parser.add_argument('-s', '--server', type=str, default='127.0.0.1', dest='server', 
        help='Radius server address')
    parser.add_argument('-P', '--port', type=int, default=0, dest='port', 
        help='Radius server auth port or acct port')
    parser.add_argument('-e', '--secret', type=str, default='secret', dest='secret', 
        help='Radius testing share secret')
    parser.add_argument('-u', '--username', type=str, default='', dest='username', 
        help='Radius testing username')
    parser.add_argument('-p', '--password', type=str, default='', dest='password', 
        help='Radius testing password')
    parser.add_argument('-n', '--requests', type=int, default=1, dest='requests', 
        help='Number of requests to perform')
    parser.add_argument('-c', '--concurrency', type=int, default=10, dest='concurrency', 
        help='Number of multiple requests to make at a time')
    parser.add_argument('-v', '--verbosity', action='store_true', default=False, dest='verbosity', 
        help='How much troubleshooting info to print')
    parser.add_argument('-t', '--timeout', type=int, default=120, dest='timeout', 
        help='Seconds to max. wait for all response')
    parser.add_argument('-conf', '--conf', type=str, default='', dest='conf', help='Radius testing config file')
    args = parser.parse_args(sys.argv[1:])

    if args.auth:
        if not args.port:
            exit(parser,1,"port must > 0")
        if not args.username:
            exit(parser,1,"username required")
        if not args.username:
            exit(parser,1,"password required")


        start_auth = lambda : auth_test(args.server,args.port,args.secret,
                args.requests,args.concurrency, args.username,args.password,args.verbosity,args.timeout)
        reactor.callLater(0.1,start_auth)
        reactor.callLater(args.timeout,reactor.stop)
        reactor.run()
        print ('testing done!')
    else:
        parser.print_help()















