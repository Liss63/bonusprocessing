package org.bonus.server;

import org.apache.xmlrpc.server.PropertyHandlerMapping;
import org.apache.xmlrpc.server.XmlRpcServer;
import org.apache.xmlrpc.server.XmlRpcServerConfigImpl;
import org.apache.xmlrpc.webserver.*;

/**
 * Created by fundaev on 13.08.15.
 */
public class App {

    public static void main(String[] args) {
        System.out.print("Starting server...");

        WebServer server = new WebServer(7080);
        XmlRpcServer xmlRpcServer = server.getXmlRpcServer();
        PropertyHandlerMapping handlerMapping = new PropertyHandlerMapping();
        try {
            handlerMapping.addHandler("card", org.bonus.server.CardHandler.class);
            xmlRpcServer.setHandlerMapping(handlerMapping);
            XmlRpcServerConfigImpl serverConfig = (XmlRpcServerConfigImpl) xmlRpcServer.getConfig();
            serverConfig.setEnabledForExtensions(true);
            serverConfig.setContentLengthOptional(false);
            server.start();
        } catch(Exception e) {
            e.printStackTrace();
        }
    }

}
