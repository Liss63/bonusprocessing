from xmlrpclib import ServerProxy
import time
import uuid
from multiprocessing import Process, freeze_support
import sys
import os

s = ServerProxy("http://localhost:7080")

def work():
    global s
    tadd = 0
    tset = 0
    tget = 0
    tinc = 0
    tdec = 0
    rcount = 10
    for i in xrange(rcount):
        cardcode = uuid.uuid4().hex
        t = time.time()
        s.card.AddCard(cardcode, 0)
        tadd += time.time() - t
        t = time.time()
        s.card.SetBalance(cardcode, 5)
        tset += time.time() - t
        t = time.time()
        s.card.IncBalance(cardcode, 2)
        tinc += time.time() - t
        t = time.time()
        s.card.DecBalance(cardcode, 7)
        tdec += time.time() - t
        t = time.time()
        s.card.GetBalance(cardcode)
        tget += time.time() - t


    print "AVG add: {0:.5f} set: {1:.5f} get: {2:.5f} inc: {3:.5f} dec {4:.5f}".format(
        tadd/rcount, tset/rcount, tget/rcount, tinc/rcount, tdec/rcount) + ' PID={0}'.format(os.getpid())

if __name__ == "__main__":
   # s = ServerProxy("http://localhost:7080")
    freeze_support()
    nproc = len(sys.argv) > 1 and int(sys.argv[1]) or 100
    print('process count ', nproc)
    print 'main process'
    procs = []
    for i in range(nproc):
        procs.append(Process(target=work))
    for i in range(nproc):
        procs[i].start()
    for i in range(nproc):
        procs[i].join()
    print('main process ended')