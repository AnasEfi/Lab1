#ifndef MESSAGE_H
#define MESSAGE_H

enum MessageTypes
{
	MT_INIT,
	MT_EXIT,
	MT_GETDATA,
	MT_DATA,
	MT_NODATA,
	MT_CONFIRM,
	MT_NOTUSER,
	MT_DISCONNECT_USER,
	STORAGE_INIT,
	MT_GETDATA_WITH_OFFSET,
	MT_CONNECT_ERROR,
	MT_NO_FOUND_MESSAGE,
	MT_AUTH_ERROR,
	MT_DATA_WITH_RESPONSE
};

enum MessageRecipients
{
	MR_BROKER = 10,
	MR_ALL = 50,
	MR_STORAGE = 80,
	MR_USER = 100
};

struct MessageHeader
{
	int to;
	int from;
	int type;
	int size;
};

class Message
{
public:
	MessageHeader header = {0};
	string data;
	
	Message() {}
	Message(int to, int from, int type = MT_DATA, const string& data = "")
	{
		this->data = data;
		header = {to, from, type, int(data.length())};
		}
	
	void send(CSocket& s)
	{
		s.Send(&header, sizeof(MessageHeader));
		if (header.size)
		{
			s.Send(data.c_str(), (int)header.size);
		}
	}

	int receive(CSocket& s)
	{
		if (!s.Receive(&header, sizeof(MessageHeader)))
		{
			return MT_NODATA;
		}
		if (header.size)
		{
			vector <char> v(header.size);
			s.Receive(&v[0], (int)header.size); //return the amount of getting bites
			data = string(&v[0], header.size);
		}
		return header.type;
	}
	static void send(CSocket& s, int to, int from, int type = MT_DATA, const string& data = "");
};

#endif // !MESSAGE_H
