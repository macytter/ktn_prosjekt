# -*- coding: utf-8 -*-
from threading import Thread

import sys


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
		self.alive = True


		self.possible_responses = {  # THESE ARE POSSIBLE COMMANDS:
			'login': self.handle_login,
			'logout': self.handle_logout,
			'msg': self.handle_message,
			'names': self.handle_names,
			'help': self.handle_help,
		}

	def command(self, text):
		list = text.split(' ', 1)
		if list[0] in self.possible_responses:
			try:
				self.possible_responses[list[0]](list[1])
			except IndexError:
				self.possible_responses[list[0]](None)

		else:
			print "Unknown command"

	def handle_login(self, login):
		payload = {
			'request': 'login',
			'content': login,
		}
		self.client.send_payload(payload)

	def handle_logout(self, unused):
		payload = {
			'request': 'logout',
			'content': None,
		}
		self.client.send_payload(payload)

	def handle_message(self, message):
		payload = {
			'request': 'msg',
			'content': message,
		}
		self.client.send_payload(payload)

	def handle_names(self, unused):
		payload = {
			'request': 'names',
			'content': None,
		}
		self.client.send_payload(payload)


	def handle_help(self, unused):
		payload = {
			'request': 'help',
			'content': None,
		}
		self.client.send_payload(payload)

	def run(self):
		while self.alive:
			try:
				msg = raw_input()
				self.command(msg)
			except SystemExit:  # GAH!! DOESNT WOOOORK.
				sys.exit()

	def kill(self):
		self.alive = False
		raise SystemExit
		sys.exit()