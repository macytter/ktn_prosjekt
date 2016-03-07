# -*- coding: utf-8 -*-
import SocketServer
import re
import json
import time
import datetime

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

userNames = []
chatHistory = []
connectedClients = {}
helpText = "login <username>, logout, msg <message>, names, help"

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

	def __init__(self):
		self.possible_responses = {  # THESE ARE SERVER RESPONSES (SERVER -> CLIENT)
			'login': self.,
            'logout': self.,
			'help': self.parse_info,
			'msg': self.parse_message,
			'names': self.parse_history,

		}

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """

        self.username = 0     # TODO denne må endres!!
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            parsed_json = json.loads(received_string)


            # TODO: Add handling of received payload from client

    def validUsername(self, username):
        if username in userNames:
            print("The username is taken")
        if not (len(username) < 16):
            print("Username must be less than 15 characters")
        if not re.match("^[A-Za-z0-9]+$", username):
            print("Username must contain characters or numbers")
        return True



    def getChatHistory(self):
        return chatHistory

    def returnHelpText(self):
        helpRespond = json.dumps(helpText)

    def responseClient(self, parsedJson):
        pass

    def returnTimeStamp(self):
        ts = time.time()
        return datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

    def sendJsonPayload(self, data):
        jSon = self.json.dumps(data)
        self.connection.send(jSon)

    def formatDict(self):
        payload= {
            'timestamp': returnTimeStamp(),
            'sender': sendJsonPayload(),
            'response': responseClient(),
            'content': self,
        }

    def getContent(self):
        pass

    def isLoggedIn(self, username):
        if username in userNames:
            return True
        return False


    def addToHistory(self, timestamp, username, msg):
        if len(chatHistory) > 8:
            del chatHistory[9]
        iter(chatHistory).first()[timestamp] = username + ": " + msg




class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True


if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
