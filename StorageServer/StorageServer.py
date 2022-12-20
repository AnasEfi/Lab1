from message import *
import cgi, pickle, cgitb, codecs, sys, datetime, os 
cgitb.enable()
#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


class StorageServer:
    def __init__(self):
        self.ClientID = 0
        self.name = "Database client"
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
        print("New message ! from id = {} to {}".format(From,To))
        with open('StoreMessageDB.db', 'ab') as f:
            pickle.dump((From,To,Data), f)



def ProcessMessages(new_client: StorageServer):
    while new_client.is_connected:
        m = new_client.SendMessage(MR_BROKER, MT_GETDATA)
        #asking: any message from server to db server
        if m.Header.Type == MT_NODATA:
            time.sleep(1)
            continue
        #save message to queue
        Message.MessegesList.append(m)
        print ('Storage server saved message. Total{}'.format(len(Message.MessegesList)))
        #update message in database
        Message.store(Message.MessegesList)
        time.sleep(1)
     

def ProcessRequest(conn, addr):
     with conn: #socket closure guarantee
          msg = Message()
          msg.Receive(conn) # gettting message from MessageServer
          print ('Requarest from {}: /To: {} / Type: {} /Text: {} '.format (msg.Header.From,msg.Header.To,msg.Header.Type,str(msg.Data)))
          foundMessage = Message.findMessage(msg.Header.From, int(msg.Data))
          if not (foundMessage is None):
              print ('Response: From {}: / To: {} /  Type: {} / Text: {}'.format(foundMessage.Header.From, foundMessage.Header.To, foundMessage.Header.Type, str(foundMessage.Data)))
          else:
              foundMessage = Message(MR_BROKER,MR_STORAGE,MT_NO_FOUND_MESSAGE,'')
          
          Message.Send(foundMessage,conn)


		    

  