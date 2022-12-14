using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using System.Net;
using System.Net.Sockets;
public enum MessageTypes : int
{
    MT_INIT,
    MT_EXIT,
    MT_GETDATA,
    MT_DATA,
    MT_NODATA,
    MT_CONFIRM,
    MT_NOTUSER,
    MT_DISCONNECT_USER

};

public enum MessageRecipients : int
{
    MR_BROKER = 10,
    MR_ALL = 50,
    MR_USER = 100
};


[StructLayout(LayoutKind.Sequential)]
struct MessageHeader
{
    [MarshalAs(UnmanagedType.I4)]
    public int to;
    [MarshalAs(UnmanagedType.I4)]
    public int from;
    [MarshalAs(UnmanagedType.I4)]
    public MessageTypes type;
    [MarshalAs(UnmanagedType.I4)]
    public int size;
};

class Message
{
    public MessageHeader header;
    public string data;
    static Encoding cp866 = null;

    Encoding get866()
    {
        if (cp866 == null)
        {
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
            cp866 = Encoding.GetEncoding("CP866");
        }
        return cp866;
    }
    public Message(int to, int from, MessageTypes type = MessageTypes.MT_DATA, string data = "")
    {
        this.data = data;
        header = new MessageHeader() { to = to, from = from, type = type, size = data.Length };
    }

    static byte[] toBytes(object obj)
    {
        int size = Marshal.SizeOf(obj);
        byte[] buff = new byte[size];
        IntPtr ptr = Marshal.AllocHGlobal(size);
        Marshal.StructureToPtr(obj, ptr, true);
        Marshal.Copy(ptr, buff, 0, size);
        Marshal.FreeHGlobal(ptr);
        return buff;
    }

    static T fromBytes<T>(byte[] buff) where T : struct
    {
        T data = default(T);
        int size = Marshal.SizeOf(data);
        IntPtr i = Marshal.AllocHGlobal(size);
        Marshal.Copy(buff, 0, i, size);
        var d = Marshal.PtrToStructure(i, data.GetType());
        if (d != null)
        {
            data = (T)d;
        }
        Marshal.FreeHGlobal(i);
        return data;
    }
    public MessageTypes receive(Socket s)
    {
        byte[] buff = new byte[Marshal.SizeOf(header)];
        if (s.Receive(buff, Marshal.SizeOf(header), SocketFlags.None) == 0)
        {
            return MessageTypes.MT_NODATA;
        }
        header = fromBytes<MessageHeader>(buff);
        if (header.size > 0)
        {
            byte[] b = new byte[header.size];
            s.Receive(b, header.size, SocketFlags.None);
            data = get866().GetString(b, 0, header.size);

        }
        return header.type;
    }

    public static void send(Socket s, int to, int from, MessageTypes type = MessageTypes.MT_DATA, string data = "")
    {
        new Message(to, from, type, data).send(s);

    }
    public void send(Socket s)
    {
        s.Send(toBytes(header), Marshal.SizeOf(header), SocketFlags.None);
        if (header.size != 0)
        {
            s.Send(get866().GetBytes(data), header.size, SocketFlags.None);
        }
    }
}
