import cgi, pickle
from os import name
from StorageServer import ProcessMessages, StorageServer
from message import *
import threading

def connection_storage():

		print ("Storage Server was connected!")
		new_client = StorageServer()
		m = new_client.SendMessage(MR_BROKER, STORAGE_INIT,name)
		
		if m.Header.Type == MT_INIT:
			print(f"\n{m.Data}")
			new_client.is_connected = True

		t = threading.Thread(target = ProcessMessages,args = (new_client,))
		t.start()
		while True:
			message = input()
			message = message.split(" ");
			command = message[0]
			match command:
				case "Send":
					data=""
					to = message[1]
					c = 2
					while c < len(message):
						data += message[c] + " "
						c += 1
					new_client.SendMessage(to, MT_DATA,data)

				case "All":
					data=""
					c = 1
					while c < len(message):
						data += message[c] + " "
						c += 1
					new_client.SendMessage(MR_ALL, MT_DATA, data)
				case "Exit":
					m=new_client.SendMessage(MR_BROKER,MT_EXIT,"")
					if m.Header.Type == MT_CONFIRM:
						new_client.is_connected = False
						print ("You was disconnected")
				case _:
					print ("Underfined")


if __name__ == "__main__":
	connection_storage()



