from message import *
import sqlite3
import cgi, pickle, cgitb, codecs, sys, datetime, os 
cgitb.enable()
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


class StorageServer:
    def __init__(self):
        self.ClientID = 0
        self.name = ""
        self.is_connected = False


    def SendMessage(self, To, Type=MT_DATA, Data=""):
        HOST = "localhost"
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

    def store(From, To, Data=""):
        with open('StoreMessageDB.db', 'ab') as f:
            pickle.dump((From,To,Data), f)

class StorageMessage:
    def __init__(self):
        self.id = 0
        self.to = 0
        self.id_from = 0
        self.data = ''

    def SetData(self, q):                # значение их формы
        self.id = q.getvalue('id')
        self.to = q.getvalue('to')
        self.title = q.getvalue('id_from')
        self.data = q.getvalue('data')
    


def ProcessMessages(new_client: StorageServer):
    while new_client.is_connected:
        m = new_client.SendMessage(MR_BROKER, MT_GETDATA)

        if m.Header.Type == MT_DATA:
            m.store(m.Header.From,m.Header.To, m.Data)
            print(m.Data)

        if m.Header.Type == MT_NOUSER:
            print("User not found")
        if m.Header.Type == MT_DISCONNECT_USER:
            m = new_client.SendMessage(MR_BROKER, MT_EXIT)
            print("Timeout you was disconnected")
            new_client.is_connected = False
        time.sleep(1)


  #  #cur = conn.cursor
  # # cur.execute(
  #      """CREATE TABLE IF NOT EXISTS users(
		##			messageid INT PRIMARY KEY,
		##			to TEXT,
		##			from TEXT,
		##			data TEXT);
		##			"""
  # # )
  # # conn.commit()
  #  new_client.is_connected = True

  # #while new_client.is_connected:
  #      m = new_client.SendMessage(MR_BROKER, MT_GETDATA)

  #      if m.Header.Type == MT_DATA:
  #    #      print(m.Data)

  #      if m.Header.Type == MT_NOUSER:
  #    #      print("User not found")
  #      if m.Header.Type == MT_DISCONNECT_USER:
  #          m = new_client.SendMessage(MR_BROKER, MT_EXIT)
  #    #      print("Timeout you was disconnected")
  #          new_client.is_connected = False
  #    #  time.sleep(1)
