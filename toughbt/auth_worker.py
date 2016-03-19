#!/usr/bin/env python
# coding=utf-8

from txzmq import ZmqEndpoint, ZmqFactory, ZmqPushConnection, ZmqPullConnection
from twisted.python import log
from twisted.internet import protocol
from twisted.internet import reactor, defer
from txradius.radius import packet
from txradius import message
from txradius.radius import dictionary,packet
import itertools
import time
import six
import time
import sys,os


class RadAuthClient(protocol.DatagramProtocol):
    def __init__(self, secret, dictionary, server, port=1812, debug=False, stat_push=None):
        self.dict = dictionary
        self.secret = six.b(secret)
        self.server = server
        self.authport = port
        self.debug = debug
        self.stat_push = stat_push
        reactor.listenUDP(0, self)

    def close(self):
        if self.transport is not None:
            self.transport.stopListening()
            self.transport = None

    def sendAuth(self, **kwargs):
        User_Password = kwargs.pop("User-Password",None)
        CHAP_Password = kwargs.pop("CHAP-Password",None)
        CHAP_Challenge = kwargs.get("CHAP-Challenge")
        request = message.AuthMessage(dict=self.dict, secret=self.secret, **kwargs)
        if User_Password:
            request['User-Password'] = request.PwCrypt(User_Password)
        if CHAP_Password:
            if CHAP_Challenge: 
                request['CHAP-Challenge'] = CHAP_Challenge
            request['CHAP-Password'] = CHAP_Password

        if self.debug:
            log.msg("Send radius Auth Request to (%s:%s): %s" % (self.server, self.authport, request.format_str()))
        self.transport.write(request.RequestPacket(), (self.server, self.authport))
        self.stat_push.push("requests")


    def datagramReceived(self, datagram, (host, port)):
        try:
            response = packet.Packet(packet=datagram,dict=self.dict, secret=self.secret)
            msgs = ['replys']
            if response.code== packet.AccessReject:
                msgs.append('rejects')
            if response.code== packet.AccessAccept:
                msgs.append('accepts')
            self.stat_push.push(",".join(msgs))
            if self.debug:
                log.msg("Received Radius Response from %s: %s" % ((host, port), message.format_packet_str(response)))
        except Exception as err:
            log.err('Invalid Response packet from %s: %s' % ((host, port), str(err)))
            self.stat_push.push("errors")



class BenchmarkWorker:

    def __init__(self,server,port,secret,requests,concurrency,username,password, verb=False,timeout=600,rate=1000):
        logname = "/tmp/trbctl-worker-{}.log".format(os.environ.get("LOGID",0))
        log.startLogging(open(logname,'w'))
        self.timeout = timeout
        self.pusher = ZmqPushConnection(ZmqFactory(), ZmqEndpoint('connect', 'ipc:///tmp/toughbt-message'))
        self.pusher.push("write worker %s log into %s" % (os.getpid(),logname))
        log.msg("init BenchmarkWorker pusher : %s " % repr(self.pusher))
        # define client cycle list
        raddict = dictionary.Dictionary(os.path.join(os.path.dirname(__file__),"dictionary"))
        new_cli = lambda : RadAuthClient(str(secret), raddict, server,port=port,debug=verb,stat_push=self.pusher)
        clis = itertools.cycle([new_cli() for c in range(concurrency)])

        # send radius message
        send = lambda:next(clis).sendAuth(**{'User-Name' : username,'User-Password':password})
        
        send_rate = 1.0/rate
        send_delay = send_rate
        for i in xrange(requests):
            reactor.callLater(send_delay,send)
            send_delay += send_rate

        reactor.callLater(self.timeout,self.on_timeout)



    def on_timeout(self):
        self.pusher.push("logger: BenchmarkWorker timeout, running times: %s" % self.timeout)
        reactor.stop()












