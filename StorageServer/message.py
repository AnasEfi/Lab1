import pickle
from dataclasses import dataclass
import socket, struct, time

MT_INIT	= 0
MT_EXIT	= 1
MT_GETDATA = 2
MT_DATA	= 3
MT_NODATA = 4
MT_CONFIRM = 5
MT_NOUSER = 6
MT_DISCONNECT_USER = 7
STORAGE_INIT = 8
MT_GETDATA_WITH_OFFSET = 9
MT_CONNECT_ERROR = 10
MT_NO_FOUND_MESSAGE = 11
MT_AUTH_ERROR = 12

MR_BROKER = 10
MR_ALL = 50
MR_STORAGE = 80
MR_USER	= 100



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

	MessegesList = []
	
	def __init__(self, To = 0, From = 0, Type = MT_DATA, Data=""):
		self.Header = MsgHeader(To, From, Type, len(Data))
		self.Data = Data

	def Send(self, s):
		self.Header.Send(s)
		if self.Header.Size > 0:
			s.send(struct.pack(f'{self.Header.Size}s', self.Data.encode('cp866')))

	def Receive(self, s):
		self.Header.Receive(s)
		if self.Header.Size > 0:
			self.Data = struct.unpack(f'{self.Header.Size}s', s.recv(self.Header.Size))[0].decode('cp866')

	def findMessage(userIdx : int, offset : int = 0):
		counter = 0
		for msg in Message.MessegesList[::-1]:
			if msg.Header.From == userIdx or msg.Header.To == userIdx or msg.Header.To == MR_ALL:
				if counter != offset:
					# Считаем до offset'a, если нужно предпоследнее сообщение, то offset = 1
					# counter пропустит первую итерацию цикла и станет +1, то есть counter будет равен 1
					# на следующей удачной итерации counter уже будет равен offset и вот это сообщение то мы и вернем
					counter += 1 
					continue
				return msg
		return None

	def load():
		try:
			with open('StoreMessageDB.db', 'rb') as f:
				Message.MessegesList = pickle.load(f)
		except FileNotFoundError:
				pass

	def store(items):
		with open('StoreMessageDB.db', 'wb') as f:
			pickle.dump(items, f)

	
	




