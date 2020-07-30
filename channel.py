class Channel:
	def __init__(self, name):	# name here is name of channel
		self.name = name
		self.messages = []

	def newMessage(self,message, sender, channel, time):
		new = {"message": message, "sender": sender, "channel": channel, "time": time}
		self.messages.append(new)
		# show only latest 100 messages from history and delete others
		while len(self.messages) > 100:
			del(self.messages[0])