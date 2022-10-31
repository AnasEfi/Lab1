import threading
from dataclasses import dataclass
import socket, struct, time
from msg import *

def ProcessMessages():
		while True:
			m = SClient.SendMessage(MR_BROKER, MT_GETDATA)
			if m.Header.Type == MT_DATA:
				print(m.Data)
			if m.Header.Type == MT_NOUSER:
				print("User not found")
			else:
				time.sleep(1)

def connection_client(new_client):

		print ("Input your name: ", end='')
		name = input()
		m = new_client.SendMessage(MR_BROKER, MT_INIT,name)
		if m.Header.Type == MT_INIT:
			print(f"\n{m.Data}")

		t = threading.Thread(target=ProcessMessages)
		t.start()
		while True:
			message = input()
			message = message.split(" ");
			command = message[0]
			match command:
				case "Send":
					data=""
					to = message[1]
					for sym in message:
						if sym == message[-1]:
							data = data + sym 
						else: data = data + sym + " "
					new_client.SendMessage(to, MT_DATA,data)
				case "All":
					data=""
					for sym in message:
						if sym == message[-1]:
							data = data + sym 
						else: data = data + sym + " "
					new_client.SendMessage(MR_ALL, MT_DATA, data)
				case _:
					print ("Underfined")
		



class SClient:
	def __init__(self):
		self.ClientID = 0
		self.name="";

	def SendMessage(self, To, Type = MT_DATA, Data=""):
		HOST = 'localhost'
		PORT = 12345
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((HOST, PORT))
			m = Message(To, self.ClientID, Type, Data)
			m.Send(s)
			m.Receive(s)
			if m.Header.Type == MT_INIT:
				self.ClientID = m.Header.To
			return m


if __name__ == "__main__":
	new_client = SClient()
	connection_client(new_client)
