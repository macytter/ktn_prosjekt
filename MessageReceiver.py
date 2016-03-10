# -*- coding: utf-8 -*-
from threading import Thread


class MessageReceiver(Thread):
	"""
	This is the message receiver class. The class inherits Thread, something that
	is necessary to make the MessageReceiver start a new thread, and it allows
	the chat client to both send and receive messages at the same time
	"""

	def __init__(self, client, connection):
		"""
		This method is executed when creating a new MessageReceiver object
		"""
		Thread.__init__(self)

		self.client = client
		self.connection = connection

		# Flag to run thread as a deamon
		self.daemon = True
		# What are daemon threads? this guy's answer is good: http://stackoverflow.com/a/190017

		# TODO: Finish initialization of MessageReceiver

		# TODO end


	def run(self):
		# TODO: Make MessageReceiver receive and handle payloads
		while(True):
			try:
				message = self.connection.recv(4096)
				self.client.receive_message(message)
			except Exception:
				# connection broke
				self.client.disconnect()

