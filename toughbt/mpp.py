#!/usr/bin/pypy
from twisted.internet import utils
from twisted.internet import protocol
import os

class MPProtocol(protocol.ProcessProtocol):
    
    def __init__(self):
        self.parent_id = os.getpid()

    def connectionMade(self):
        print "benckmark worker created! master pid - %s, worker pid - %s" %(self.parent_id, self.transport.pid)

    def outReceived(self, data):
        pass

    def errReceived(self, data):
        print "worker error", data

    def processExited(self, reason):
        print "benckmark worker exit %s, status %d" % (self.transport.pid, reason.value.exitCode,)

    def processEnded(self, reason):
        print "benckmark %s worker ended, status %d" % (self.transport.pid, reason.value.exitCode,)

    

