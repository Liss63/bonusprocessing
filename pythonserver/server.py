from twisted.web.xmlrpc import XMLRPC, withRequest
from twisted.web.server import Site
from txmongo.connection import ConnectionPool
from twisted.internet import defer
from pymongo import ReturnDocument

class BonusProcessing(XMLRPC):
    """
    An example object to be published.
    """

    connection = None
    db = None
    cardscollection = None

    def __init__(self, allowNone=False, useDateTime=False):
        XMLRPC.__init__(self, allowNone, useDateTime)
        connection = ConnectionPool()
        self.db = connection.bonusprocessing
        self.cardscollection = self.db.cards

    @withRequest
    @defer.inlineCallbacks
    def xmlrpc_echo(self, request, x):
        """
        Return all passed args.
        """
        print 'Call echo'
        print request.getClientIP()
        res = yield x
        defer.returnValue(res)

    @withRequest
    @defer.inlineCallbacks
    def xmlrpc_AddCard(self, request, code, balance):
        """
        Add card and return true
        """
        print 'Call AddCard'
        print request.getClientIP()

        res = None
        try:
            self.cardscollection.insert({"code": code, "balance": balance})
            res = yield True
        except:
            res = yield False

        defer.returnValue(res)

    @withRequest
    @defer.inlineCallbacks
    def xmlrpc_GetBalance(self, request, code):
        """
        Get balance by card code
        """
        balance = 0

        print 'Call GetBalance'
        print request.getClientIP()

        card = yield self.cardscollection.find_one({"code":code})
        print card
        if card != None:
            res = yield card['balance']

        defer.returnValue(res)

    @withRequest
    @defer.inlineCallbacks
    def xmlrpc_SetBalance(self, request, code, balance):
        """
        Set balance by card code
        """
        print 'Call SetBalance'
        print request.getClientIP()

        self.cardscollection.find_one_and_update(
            {"code": code},
            {"$set": {"balance": balance}}
        )

        res = yield True
        defer.returnValue(res)

    @withRequest
    @defer.inlineCallbacks
    def xmlrpc_IncBalance(self, request, code, inc_value):
        """
        Int balance by code
        """
        balance = inc_value

        print 'Call IncBalance'
        print request.getClientIP()

        rec = yield self.cardscollection.find_one_and_update(
            {"code": code},
            {"$inc": {"balance": inc_value}},
            return_document=ReturnDocument.AFTER
        )

        print rec

        res = yield rec['balance']
        defer.returnValue(res)

    @withRequest
    @defer.inlineCallbacks
    def xmlrpc_DecBalance(self, request, code, dec_value):
        """
        Dec balance by code
        """
        balance = dec_value
        print 'Call DecBalance'
        print request.getClientIP()
        rec = yield self.cardscollection.find_one_and_update(
            {"code": code},
            {"$inc": {"balance": -dec_value}},
            return_document=ReturnDocument.AFTER
        )

        print rec

        res = yield rec['balance']
        defer.returnValue(res)

    @withRequest
    def xmlrpc_add(self, request, a, b):
        """
        Return sum of arguments.
        """
        print 'Call Add'
        print request.getClientIP()

        return a + b


if __name__ == '__main__':
    from twisted.internet import reactor

    r = BonusProcessing()
    reactor.listenTCP(7080, Site(r))
    reactor.run()