import json


class MessageParser():
	def __init__(self, client):
		self.possible_responses = {  # THESE ARE SERVER RESPONSES (SERVER -> CLIENT)
			'error': self.parse_error,
			'info': self.parse_info,
			'message': self.parse_message,
			'history': self.parse_history,
		}

		self.client = client

	def encode(self, payload):
		return json.dumps(payload)  # encode to json

	def parse(self, json_string):
		payload = json.loads(json_string)  # decode the JSON object

		if payload['response'] in self.possible_responses:
			return self.possible_responses[payload['response']](payload)
		else:
			return "Error: unknown response. Response was: " + payload['response']

	# ALL parse_xxx methods below are HELPER methods for the parse method!

	def parse_error(self, payload):
		timestamp = payload["timestamp"]
		message = payload["content"]

		return "[{}][SERVER] ERROR: {}".format(timestamp, message)

	def parse_info(self, payload):
		timestamp = payload["timestamp"]
		message = payload["content"]

		# login successful
		if message == "Login successful":
			self.client.userLoggedIn = True
			payload = {
				'request': 'history',
				'content': None,
			}
			self.client.send_payload(payload)

		# logout successful
		if message == "Logout successful":
			self.client.userLoggedIn = False

		return "[{}][SERVER]: {}".format(timestamp, message)

	def parse_message(payload):
		timestamp = payload["timestamp"]
		sender = payload["sender"]
		message = payload["content"]
		return "[{}][{}]: {}".format(timestamp, sender, message)

	def parse_history(self, payload):
		history = payload["content"]
		history_list = list("")
		for history_payload in history:
			history_list.append(self.parse_message(history_payload))
		return "\n".join(history_list)  # join with new line as separator