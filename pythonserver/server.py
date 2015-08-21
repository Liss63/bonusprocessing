from twisted.web.xmlrpc import XMLRPC, withRequest
from twisted.web.server import Site
from txmongo.connection import ConnectionPool
from twisted.internet import defer
from pymongo import ReturnDocument
from twisted.python.util import println


class DefaultHandler(XMLRPC):
    @withRequest
    @defer.inlineCallbacks
    def xmlrpc_echo(self, request, x):
        """
        Return all passed args.
        """
        println('Call echo ' + repr(request.getClientIP()))
        defer.returnValue((yield x))


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
    def xmlrpc_AddCard(self, request, code, balance):
        """
        Add card and return true
        """
        println('Call AddCard ' + repr(request.getClientIP() + ' card ' + repr(code)))

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
        println('Call GetBalance ' + repr(request.getClientIP()) + ' card ' + repr(code))
        card = yield self.cardscollection.find_one({"code":code})
        res = yield card['balance']
        defer.returnValue(res)

    @withRequest
    @defer.inlineCallbacks
    def xmlrpc_SetBalance(self, request, code, balance):
        """
        Set balance by card code
        """
        println('Call SetBalance' + repr(request.getClientIP()) + ' card ' + repr(code) + ' balance ' + repr(balance))

        self.cardscollection.find_one_and_update(
            {"code": code},
            {"$set": {"balance": balance}}
        )

        defer.returnValue((yield True))

    @withRequest
    @defer.inlineCallbacks
    def xmlrpc_IncBalance(self, request, code, inc_value):
        """
        Inc balance by code
        """
        println('Call IncBalance' + repr(request.getClientIP()) + ' card ' + repr(code) + ' balance ' + repr(inc_value))

        rec = yield self.cardscollection.find_one_and_update(
            {"code": code},
            {"$inc": {"balance": inc_value}},
            return_document=ReturnDocument.AFTER
        )

        res = yield rec['balance']
        defer.returnValue(res)

    @withRequest
    @defer.inlineCallbacks
    def xmlrpc_DecBalance(self, request, code, dec_value):
        """
        Dec balance by code
        """
        println('Call DecBalance' + repr(request.getClientIP()) + ' card ' + repr(code) + ' balance ' + repr(dec_value))

        rec = yield self.cardscollection.find_one_and_update(
            {"code": code},
            {"$inc": {"balance": -dec_value}},
            return_document=ReturnDocument.AFTER
        )

        res = yield rec['balance']
        defer.returnValue(res)


if __name__ == '__main__':
    from twisted.internet import reactor

    r = DefaultHandler()
    r.putSubHandler('card', BonusProcessing())
    reactor.listenTCP(7080, Site(r))
    reactor.run()