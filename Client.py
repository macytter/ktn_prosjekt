# -*- coding: utf-8 -*-
import socket
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

		self.messageReceiver = MessageReceiver(self, self.connection) # is a thread by itself.
		self.userInput = UserInput(self) # is a thread by itself.

		self.parser = MessageParser()

		self.run()

	def run(self):

		# Initiate the connection to the server
		self.connection.connect((self.host, self.server_port))
		self.messageReceiver.start() # start the thread
		self.userInput.start() # start the thread


	def disconnect(self):
		# TODO: Handle disconnection
		self.connection.close()
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
