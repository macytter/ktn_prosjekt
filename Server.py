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
helpText = "Available commands: login <username>, logout, msg <message>, names, help"


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
			try:
				received_string = self.connection.recv(4096)
				parsed_json = json.loads(received_string)
				self.handleRequest(parsed_json)
			except Exception:
				# connection broke

				if self.username in userNames:
					userNames.remove(self.username)
				self.finish()


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

		response_payload1 = {
			'timestamp': self.returnTimeStamp(),
			'sender': 'server',
			'response': None,
			'content': None,
		}


		if username in userNames:
			# reply "username taken"
			response_payload1["response"] = "error"
			response_payload1["content"] = "Username taken"

		elif not (len(username) < 16):
			# reply "username too long
			response_payload1["response"] = "error"
			response_payload1["content"] = "Username too long"

		elif not re.match("^[A-Za-z0-9]+$", username):
			# reply username must contain characters or numbers
			response_payload1["response"] = "error"
			response_payload1["content"] = "username must contain characters or numbers"

		else:
			# username okay, user logged in
			response_payload1["response"] = "info"
			response_payload1["content"] = "Login successful"
			self.username = payload["content"]
			print "assigning username: " + self.username
			userNames.append(payload["content"])
			# add client to client list
			connectedClients[self.username] = self.connection

		self.sendJsonPayload(response_payload1)

		# send only history log and user login broadcast if logged in successfully
		if (self.username in userNames) and len(chatHistory) > 0:
			response_payload2 = {
				'timestamp': self.returnTimeStamp(),
				'sender': 'server',
				'response': 'history',
				'content': chatHistory
			}
			print response_payload2
			self.sendJsonPayload(response_payload2)

			# user login broadcast
			response_payload3 = {
				'timestamp': self.returnTimeStamp(),
				'sender': 'server',
				'response': 'info',
				'content': "User connected: " + self.username,
			}
			print "broadcasting login"
			self.sendJsonPayloadToAll(response_payload3)



	def handle_logout(self, payload):
		print "Logging user out"
		if self.username in userNames:
			userNames.remove(self.username)
			connectedClients.pop(self.username)
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
		if self.username in userNames:
			response_payload = {
				'timestamp': self.returnTimeStamp(),
				'sender': self.username,
				'response': 'message',
				'content': payload["content"],
			}
			chatHistory.append(json.dumps(response_payload))
			if len(chatHistory) > 10:
				chatHistory.pop(0)
			self.sendJsonPayloadToAll(response_payload)
		else:
			response_payload = {
				'timestamp': self.returnTimeStamp(),
				'sender': 'server',
				'response': 'error',
				'content': "Not logged in.",
			}
			self.sendJsonPayload(response_payload)

	def handle_names(self, payload):
		response_payload = {
			'timestamp': self.returnTimeStamp(),
			'sender': 'server',
			'response': 'info',
			'content': "Online users: " + ", ".join(userNames),
		}
		self.sendJsonPayload(response_payload)

	def returnTimeStamp(self):
		ts = time.time()
		return datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

	def sendJsonPayload(self, data):
		self.connection.send(json.dumps(data))

	def sendJsonPayloadToAll(self, data):
		jSon = json.dumps(data)
		for con in connectedClients.values():
			con.send(jSon)

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
