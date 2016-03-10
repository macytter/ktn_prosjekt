# -*- coding: utf-8 -*-
import socket

import sys

from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
from UserInput import UserInput


class Client:
	"""
	This is the chat client class
	"""

	def __init__(self, host, server_port):
		"""
		This method is run when creating a new Client object
		"""

		# Set up the socket connection to the server
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = host
		self.server_port = server_port

		self.userLoggedIn = False

		self.messageReceiver = MessageReceiver(self, self.connection)  # is a thread by itself.
		self.userInput = UserInput(self)  # is a thread by itself.

		self.parser = MessageParser(self)

		self.run()

	def run(self):
		# Initiate the connection to the server
		try:
			self.connection.connect((self.host, self.server_port))
		except:
			print "No connection to the server were established. Exiting."
			sys.exit()

		self.messageReceiver.start()  # start the thread
		self.userInput.start()  # start the thread

		print "Client Ready. Please type command. type 'help' to view server commands."

	def disconnect(self):
		self.connection.close()
		print "Server disconnected"
		self.userInput.kill()
		sys.exit()
		pass

	def receive_message(self, message):
		parsed_message = self.parser.parse(message)
		print parsed_message

	def send_payload(self, data):
		json = self.parser.encode(data)
		self.connection.send(json)
		pass

	# More methods may be needed!


if __name__ == '__main__':
	"""
	This is the main method and is executed when you type "python Client.py"
	in your terminal.

	No alterations are necessary
	"""
	client = Client('localhost', 9998)
