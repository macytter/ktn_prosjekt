# -*- coding: utf-8 -*-
from threading import Thread


class UserInput(Thread):
	"""
	This is the user input class. The class inherits Thread, something that
	is necessary to make the MessageReceiver start a new thread, and it allows
	the chat client to both send and receive messages at the same time



	this class handles user input and delivers user commands to the client

	"""

	def __init__(self, client):
		"""
		This method is executed when creating a new UserInput object
		"""
		Thread.__init__(self)

		self.client = client

	def run(self):
		while(True):
			msg = raw_input("command: ")
			# TODO: add checks (see messageParser) for available commands, and call method
