package org.bonus.server;

import com.mongodb.*;
import org.apache.log4j.Logger;

/**
 * Created by fundaev on 17.08.15.
 */
public class CardHandler {

    private MongoClient connection = null;

    public CardHandler() {
        Logger.getLogger("CardHandler").debug("CardHandler has been created");
    }

    public boolean AddCard(String code, int balance) {
        System.out.println(String.format("Call AddCard: code=%s, balance=%d", code, balance));
        boolean res = true;
        try {
            BasicDBObject doc = new BasicDBObject("code", code).append("balance", new Integer(balance));
            getCardsCollection().insert(doc);
        } catch (Exception e) {
            e.printStackTrace();
            res = false;
        }

        closeConnection();
        return res;
    }

    public Integer GetBalance(String code) {
        System.out.println(String.format("Call GetBalance: code=%s", code));
        try {
            BasicDBObject doc = new BasicDBObject("code", code);
            DBObject obj = getCardsCollection().findOne(doc);
            closeConnection();
            return (obj != null ? new Integer(obj.get("balance").toString()) : 0);
        } catch (Exception e) {
            e.printStackTrace();
        }

        closeConnection();
        return new Integer(0);
    }

    public boolean SetBalance(String code, int balance) {
        System.out.println(String.format("Call SetBalance: code=%s, balance=%d", code, balance));
        boolean res = true;
        try {
            BasicDBObject modify = new BasicDBObject("code", code).append("balance", new Integer(balance));
            getCardsCollection().findAndModify(new BasicDBObject("code", code), modify);
        } catch (Exception e) {
            e.printStackTrace();
            res = false;
        }

        closeConnection();
        return res;
    }


    public boolean IncBalance(String code, Integer inc) {
        System.out.println(String.format("Call IncBalance: code=%s, inc=%d", code, inc));
        boolean res = true;
        try {
            DBObject modify = new BasicDBObject("$inc", new BasicDBObject("balance", inc));
            getCardsCollection().update(new BasicDBObject("code", code), modify);
        } catch (Exception e) {
            e.printStackTrace();
            res = false;
        }

        closeConnection();
        return res;
    }

    public boolean DecBalance(String code, int dec) {
        System.out.println(String.format("Call DecBalance: code=%s, dec=%d", code, dec));
        boolean res = true;
        try {
            DBObject modify = new BasicDBObject("$inc", new BasicDBObject("balance", new Integer(-dec)));
            getCardsCollection().update(new BasicDBObject("code", code), modify);
        } catch (Exception e) {
            e.printStackTrace();
            res = false;
        }

        closeConnection();
        return res;
    }

    private MongoClient getConnection() {
        if (this.connection != null)
            return this.connection;

        try {
            this.connection = new MongoClient();
            this.connection.setWriteConcern(WriteConcern.JOURNALED);
        } catch (Exception e) {
            Logger.getLogger(CardHandler.class.getName()).error("Failed to open MongoDB connection");
            e.printStackTrace();
        }

        return this.connection;
    }

    private void closeConnection() {
        if (this.connection != null)
            this.connection.close();
    }

    private DBCollection getCardsCollection() throws Exception {
        DB db = getConnection().getDB("bonusprocessing");
        return db.getCollection("cards");
    }

}
