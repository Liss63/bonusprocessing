from xmlrpclib import ServerProxy
import time
import uuid
from multiprocessing import Process, freeze_support, Queue
import sys
import os

s = ServerProxy("http://localhost:7080")

def work(rcount, qadd, qset, qget, qinc, qdec):
    global s
    tadd = 0
    tset = 0
    tget = 0
    tinc = 0
    tdec = 0
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

    qadd.put(tadd/rcount)
    qset.put(tset/rcount)
    qget.put(tget/rcount)
    qinc.put(tinc/rcount)
    qdec.put(tdec/rcount)
#    print "AVG add: {0:.5f} set: {1:.5f} get: {2:.5f} inc: {3:.5f} dec {4:.5f}".format(
#        tadd/rcount, tset/rcount, tget/rcount, tinc/rcount, tdec/rcount) + ' PID={0}'.format(os.getpid())

if __name__ == "__main__":
   # s = ServerProxy("http://localhost:7080")
    freeze_support()
    nproc = len(sys.argv) > 1 and int(sys.argv[1]) or 100
    rcount = len(sys.argv) > 2 and int(sys.argv[2]) or 100
    print('Number of processes: ', nproc)
    print('Number of measurements: ', rcount)
    print 'main process'
    procs = []
    qadd = Queue()
    qset = Queue()
    qget = Queue()
    qinc = Queue()
    qdec = Queue()
    for i in range(nproc):
        procs.append(Process(target=work, args=(rcount, qadd, qset, qget, qinc, qdec)))
    for i in range(nproc):
        procs[i].start()
    for i in range(nproc):
        procs[i].join()

    madd = 0
    mset = 0
    mget = 0
    minc = 0
    mdec = 0
    for i in range(nproc):
        madd += qadd.get()
        mset += qset.get()
        mget += qget.get()
        minc += qinc.get()
        mdec += qdec.get()
    assert (qadd.empty),"qadd queue is not empty"
    assert (qset.empty),"qset queue is not empty"
    assert (qget.empty),"qget queue is not empty"
    assert (qinc.empty),"qinc queue is not empty"
    assert (qdec.empty),"qdec queue is not empty"

    print("Avarage time:")
    print("AddCard:    {0:.5f}".format(madd/nproc))
    print("SetBalance: {0:.5f}".format(mset/nproc))
    print("GetBalance: {0:.5f}".format(mget/nproc))
    print("IncBalance: {0:.5f}".format(minc/nproc))
    print("DecBalance: {0:.5f}".format(mdec/nproc))

    print('main process ended')
