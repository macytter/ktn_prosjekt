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

	def handle(self):
		"""
		This method handles the connection between a client and the server.
		"""

		self.possible_requests = {  # THESE ARE SERVER RESPONSES (SERVER -> CLIENT)
			'login': self.handle_login,
			'logout': self.handle_logout,
			'help': self.handle_help,
			'msg': self.handle_msg,
			'names': self.handle_names,

		}


		self.username = None
		self.ip = self.client_address[0]
		self.port = self.client_address[1]
		self.connection = self.request

		# Loop that listens for messages from the client
		while True:
			received_string = self.connection.recv(4096)
			parsed_json = json.loads(received_string)
			self.handleRequest(parsed_json)


	def handleRequest(self, payload):
		if payload['request'] in self.possible_requests:
			self.possible_requests[payload['request']](payload)
		else:
			# error response
			error_response = {
				'timestamp': self.returnTimeStamp(),
				'sender': 'server',
				'response': 'error',
				'content': 'Unknown request: ' + payload['request'],
			}
			self.sendJsonPayload(error_response)

	def handle_login(self, payload):

		username = payload["content"]

		response_payload = {
			'timestamp': self.returnTimeStamp(),
			'sender': 'server',
			'response': None,
			'content': None,
		}


		if username in userNames:
			# reply "username taken"
			response_payload["response"] = "error"
			response_payload["content"] = "Username taken"

		elif not (len(username) < 16):
			# reply "username too long
			response_payload["response"] = "error"
			response_payload["content"] = "Username too long"

		elif not re.match("^[A-Za-z0-9]+$", username):
			# reply username must contain characters or numbers
			response_payload["response"] = "error"
			response_payload["content"] = "username must contain characters or numbers"

		else:
			# username okay, user logged in
			response_payload["response"] = "info"
			response_payload["content"] = "Login successful"
			self.username = payload["content"]
			userNames.append(payload["content"])

		self.sendJsonPayload(response_payload)

		# send only history log if logged in successfully
		if self.username in userNames:
			response_payload = {
				'timestamp': self.returnTimeStamp(),
				'sender': 'server',
				'response': 'history',
				'content': chatHistory,
			}
			self.sendJsonPayload(response_payload)




	def handle_logout(self, payload):
		print "TEST: username: " + self.username
		if self.username in userNames:
			userNames.remove(self.username)
			response_payload = {
				'timestamp': self.returnTimeStamp(),
				'sender': 'server',
				'response': 'info',
				'content': 'Logout successful',
			}
			self.sendJsonPayload(response_payload)
		else:
			response_payload = {
				'timestamp': self.returnTimeStamp(),
				'sender': 'server',
				'response': 'error',
				'content': 'User not logged in',
			}
			self.sendJsonPayload(response_payload)

	def handle_help(self, payload):
		response_payload = {
			'timestamp': self.returnTimeStamp(),
			'sender': 'server',
			'response': 'info',
			'content': helpText,
		}
		self.sendJsonPayload(response_payload)


	def handle_msg(self, payload):
		pass

	def handle_names(self, payload):
		response_payload = {
			'timestamp': self.returnTimeStamp(),
			'sender': 'server',
			'response': 'info',
			'content': ", ".join(userNames),
		}
		self.sendJsonPayload(response_payload)

	def returnTimeStamp(self):
		ts = time.time()
		return datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

	def sendJsonPayload(self, data):
		jSon = json.dumps(data)
		self.connection.send(jSon)


	def sendJsonPayloadToAll(self, data):
		jSon = json.dumps(data)
		self.connection.send(jSon)



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

