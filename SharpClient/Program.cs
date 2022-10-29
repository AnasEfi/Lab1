using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Xml.Linq;

class Program
{
    static void Main(string[] args)
    {
        Console.Write("Enter your name: ");
        Client client = new Client
        {
            name = Console.ReadLine()
        };

        var m = client.send((int)MessageRecipients.MR_BROKER, MessageTypes.MT_INIT);
        if (m.header.type != MessageTypes.MT_INIT)
        {
            Console.WriteLine("Error in name!");
        }
        Console.WriteLine(m.data);

        Thread t = new Thread(() => ProcessMessages(client));
        t.Start();

        while (true)
        {
            if (client.SUPER_FLAG_IS_DISCONNECTED)
                return;
            var s = Console.ReadLine();
            if (s != null)
            {
                var splitIdx = s.IndexOf(' ');
                string to;

                if (splitIdx != -1)

                {
                    to = s.Substring(0, splitIdx);
                    switch (to)
                    {
                        case "Send":
                            s = s.Substring(splitIdx + 1, s.Length - splitIdx - 1);
                            var sendTo = s.Substring(0, splitIdx);
                            splitIdx = s.IndexOf(' ');
                            s = s.Substring(splitIdx + 1, s.Length - splitIdx - 1);
                            if (int.TryParse(sendTo, out int idTo))
                            {
                                if (idTo == (int)client.ClientID)
                                {
                                    Console.WriteLine("You cant send message to yourself!");
                                    break;
                                }
                                client.send(idTo, MessageTypes.MT_DATA, s);
                            }
                            else Console.WriteLine("Invalid ID");
                            break;
                        case "All":
                            s = s.Substring(splitIdx + 1, s.Length - splitIdx - 1);
                            client.send((int)MessageRecipients.MR_ALL, MessageTypes.MT_DATA, s);
                            break;

                        default:
                            Console.WriteLine("Wrong command!");
                            break;
                    }

                }
                else
                {
                    Message mFromServer = client.send((int)MessageRecipients.MR_BROKER, MessageTypes.MT_EXIT);
                    if (mFromServer.header.type == MessageTypes.MT_CONFIRM)
                    {
                        Console.WriteLine("You was disconnected");
                        client.SUPER_FLAG_IS_DISCONNECTED = true;
                        Thread.Sleep(1000);
                        return;
                    }
                }
            }
        }
    }
    static void ProcessMessages(Client currentClient)
    {
        while (true)
        {
            if (currentClient.SUPER_FLAG_IS_DISCONNECTED != true)
            {
                Thread.Sleep(1000);
                var m = currentClient.send((int)MessageRecipients.MR_BROKER, MessageTypes.MT_GETDATA);
                switch (m.header.type)
                {

                    case MessageTypes.MT_DATA:
                        Console.WriteLine(m.data);
                        break;
                    case MessageTypes.MT_NOTUSER:
                        Console.WriteLine("No user found");
                        break;
                    case MessageTypes.MT_DISCONNECT_USER:
                        {
                            Console.WriteLine("Timeout, you was disconnected");
                            currentClient.send((int)MessageRecipients.MR_BROKER, MessageTypes.MT_EXIT, "");
                            currentClient.SUPER_FLAG_IS_DISCONNECTED = true;
                            Thread.Sleep(1000);
                            return;
                        }
                    case MessageTypes.MT_CONFIRM:
                        return;
                    default:
                        Thread.Sleep(100);
                        break;
                }
            }
            else return;
        }

    }
}

