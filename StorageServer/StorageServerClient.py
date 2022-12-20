
from os import name
from StorageServer import ProcessMessages, StorageServer, ProcessRequest
from message import *
import threading 


def StartStorageServerSocket():
	HOST = '127.0.0.1'
	PORT = 50007
	while True:
		with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
			s.bind ((HOST,PORT))
			s.listen()
			conn, addr = s.accept()
			serverThread = threading.Thread(target=ProcessRequest,args = (conn,addr, ))
			serverThread.start()

def connection_storage():

		print ("Storage Server was connected!")
		new_client = StorageServer()
		m = new_client.SendMessage(MR_BROKER, STORAGE_INIT,name)
		
		if m.Header.Type == MT_INIT:
			print(f"\n{m.Data}")
			new_client.is_connected = True

		Message.load() #loading database
		print ('Database download! Theare are {} message in a base'.format(len(Message.MessegesList)))

		t = threading.Thread(target = ProcessMessages,args = (new_client,)) # thread to send message to MessageServer 
		t.start()

		StartStorageServerSocket() # socket to get messages from MessageServer

if __name__ == "__main__":
	connection_storage()



