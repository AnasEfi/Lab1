import threading
from dataclasses import dataclass
import socket, struct, time
from msg import *
from Client import *

def connection_client():

		print ("Input your name: ", end='')
		name = input()
		new_client = SClient();
		m = new_client.SendMessage(MR_BROKER, MT_INIT,name)
		if m.Header.Type == MT_INIT:
			print(f"\n{m.Data}")
			new_client.is_connected = True

		t = threading.Thread(target=ProcessMessages,args = (new_client,))
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
	connection_client()
