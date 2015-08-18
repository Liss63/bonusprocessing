package org.bonus.server;

import com.mongodb.*;

/**
 * Created by fundaev on 17.08.15.
 */
public class CardHandler {
    public boolean AddCard(String code, int balance) {
        System.out.println(String.format("Call AddCard: code=%s, balance=%d", code, balance));
        try {
            BasicDBObject doc = new BasicDBObject("code", code).append("balance", new Integer(balance));
            getCardsCollection().insert(doc);
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }

        return true;
    }

    public Integer GetBalance(String code) {
        System.out.println(String.format("Call GetBalance: code=%s", code));
        try {
            BasicDBObject doc = new BasicDBObject("code", code);
            DBObject obj = getCardsCollection().findOne(doc);
            return (obj != null ? new Integer(obj.get("balance").toString()) : 0);
        } catch (Exception e) {
            e.printStackTrace();
        }

        return new Integer(0);
    }

    public boolean SetBalance(String code, int balance) {
        System.out.println(String.format("Call SetBalance: code=%s, balance=%d", code, balance));
        try {
            BasicDBObject modify = new BasicDBObject("code", code).append("balance", new Integer(balance));
            getCardsCollection().findAndModify(new BasicDBObject("code", code), modify);
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }

        return true;
    }


    public boolean IncBalance(String code, Integer inc) {
        System.out.println(String.format("Call IncBalance: code=%s, inc=%d", code, inc));
        try {
            DBObject modify = new BasicDBObject("$inc", new BasicDBObject("balance", inc));
            getCardsCollection().update(new BasicDBObject("code", code), modify);
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }

        return true;
    }

    public boolean DecBalance(String code, int dec) {
        System.out.println(String.format("Call DecBalance: code=%s, dec=%d", code, dec));
        try {
            DBObject modify = new BasicDBObject("$inc", new BasicDBObject("balance", new Integer(-dec)));
            getCardsCollection().update(new BasicDBObject("code", code), modify);
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }

        return true;
    }

    private DBCollection getCardsCollection() throws Exception {
        MongoClient client = new MongoClient();
        client.setWriteConcern(WriteConcern.JOURNALED);
        DB db = client.getDB("bonusprocessing");
        return db.getCollection("cards");
    }

}
