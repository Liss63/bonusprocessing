from xmlrpclib import ServerProxy
import time
import uuid

class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print "Elapsed time: {:.3f} sec".format(time.time() - self._startTime)

if __name__ == "__main__":
    s = ServerProxy("http://localhost:7080")
    tadd = 0
    tset = 0
    tget = 0
    tinc = 0
    tdec = 0
    rcount = 20
    for i in xrange(rcount):
        cardcode = uuid.uuid1().hex
        t = time.time()
        s.AddCard(cardcode, 0)
        tadd += time.time() - t
        t = time.time()
        s.SetBalance(cardcode, 5)
        tset += time.time() - t
        t = time.time()
        s.DecBalance(cardcode, 1)
        tdec = time.time() - t
        t = time.time()
        s.GetBalance(cardcode)
        tget += time.time() - t
        t = time.time()
        s.IncBalance(cardcode, 2)
        tinc += time.time() - t

    print "AVG add: {:.5f} sec".format(tadd/rcount)
    print "AVG set: {:.5f} sec".format(tset/rcount)
    print "AVG get: {:.5f} sec".format(tget/rcount)
    print "AVG inc: {:.5f} sec".format(tinc/rcount)
    print "AVG dec: {:.5f} sec".format(tdec/rcount)