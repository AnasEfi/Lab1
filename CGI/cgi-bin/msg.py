import threading
from dataclasses import dataclass
import socket, struct, time
from msg import *

MT_INIT	= 0
MT_EXIT	= 1
MT_GETDATA = 2
MT_DATA	= 3
MT_NODATA = 4
MT_CONFIRM = 5
MT_NOUSER = 6
MT_DISCONNECT_USER = 7
MT_GETDATA_WITH_OFFSET = 9
MT_CONNECT_ERROR = 10
MT_NO_FOUND_MESSAGE = 11
MT_AUTH_ERROR = 12
MT_DATA_WITH_RESPONSE = 13


MR_BROKER = 10
MR_ALL = 50
MR_USER	= 100
MR_STORAGE = 80

@dataclass
class MsgHeader:
	To: int = 0	
	From: int = 0
	Type: int = 0
	Size: int = 0

	def Send(self, s):
		s.send(struct.pack(f'iiii', int(self.To), int(self.From), int(self.Type), int(self.Size)))

	def Receive(self, s):
		try:
			(self.To, self.From, self.Type, self.Size) = struct.unpack('iiii', s.recv(16))
		except:
			self.Size = 0
			self.Type = MT_NODATA

class Message:

	Data: str #annotation of the type
	
	def __init__(self, To = 0, From = 0, Type = MT_DATA, Data=""):
		self.Header = MsgHeader(To, From, Type, len(str(Data)))
		self.Data = Data

	def Send(self, s):
		self.Header.Send(s)
		if self.Header.Size > 0:
			s.send(struct.pack(f'{self.Header.Size}s', str(self.Data).encode('cp866')))

	def Receive(self, s):
		self.Header.Receive(s)
		if self.Header.Size > 0:
			self.Data = struct.unpack(f'{self.Header.Size}s', s.recv(self.Header.Size))[0].decode('cp866')



