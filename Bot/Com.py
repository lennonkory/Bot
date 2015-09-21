import os
from socket import *

class Com:

	def __init__(self, port = 13000, host = "192.168.0.101"):
		"""
		This constructor initiatizes addr (the addresss of the server) and UDPSock (how 
		the client talks to the server)
		
		Args:
			port(int): an open port (may need to be changed)
			host(string): IP address of the SERVER. will need to be updated before we run the bot.

		"""
		self.addr = (host, port)
		self.UDPSock = socket(AF_INET, SOCK_DGRAM)

	"""
		for now the following two functions do the exact same thing.
		I think it maybe best to only have one function call the server and based on what message
		the client sends have the server parse it and perform the right operations
	"""
	def sendMessage(self, message):
		self.UDPSock.sendto(str(message), self.addr)

	def updateMap(self,data):
		#data needs to be turn into a string (for now)
		self.UDPSock.sendto(str(data), self.addr)

	def end(self):
		"""
			This function simply closes the socket
		"""
		self.UDPSock.close()
		os._exit(0)