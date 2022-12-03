
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Net;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

class Client
{
    public string name;
    public int ClientID;
    public bool isConnected = false;

    public Message send(int to, MessageTypes type = MessageTypes.MT_DATA, string data = "")
    {
        int nPort = 12345;
        IPEndPoint endPoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), nPort);
        Socket s = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        s.Connect(endPoint);
        if (!s.Connected)
        {
            throw new Exception("Connection error");
        }
        var m = new Message(to, ClientID, type, data);

        m.send(s);
        if (m.receive(s) == MessageTypes.MT_INIT)
        {
            ClientID = m.header.to;
        }
        if (m.receive(s) == MessageTypes.MT_CONFIRM)
        {
            m.header.type = MessageTypes.MT_EXIT;
        }
        return m;
    }
}