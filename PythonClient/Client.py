from msg import *

class SClient:
	def __init__(self):
		self.ClientID = 0;
		self.name="";
		self.is_connected = False;

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
			if m.Header.Type == MT_EXIT:
				m.Header.Type = MT_CONFIRM
		return m


def ProcessMessages(new_client : SClient):
		while new_client.is_connected: 
			m = new_client.SendMessage(MR_BROKER, MT_GETDATA)
			if m.Header.Type == MT_DATA:
				print(m.Data)
			if m.Header.Type == MT_NOUSER:
				print("User not found")
			if m.Header.Type == MT_DISCONNECT_USER:
				m = new_client.SendMessage(MR_BROKER, MT_EXIT)
				print("Timeout you was disconnected")
				new_client.is_connected = False
			time.sleep(1)

