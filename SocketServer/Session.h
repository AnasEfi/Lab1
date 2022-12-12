#ifndef SESSION_H
#define SESSION_H


#include "Message.h"
class Session
{
public:
	int id;
	string name;// опциональное имя при старте
	queue<Message> messages;
	long long lastInteractionTime;
	bool isConnected = false;

	CCriticalSection cs; //во время чтения сообщения из очереди НИКТО не писал сообщение
	Session(int _id, string _name)
		:id(_id), name(_name)
	{
	}

	void add(Message& m) 
	{
		CSingleLock lock(&cs, TRUE);
		messages.push(m);
	}

	void send(CSocket& s)
	{
		CSingleLock lock(&cs, TRUE);
		if (messages.empty())
		{
			Message::send(s, id, MR_BROKER, MT_NODATA);
		}
		else
		{
			Message m = messages.front();

			string dataFromQueue = "Message from [" + to_string(m.header.from) + "]: " + m.data;
			m.data = dataFromQueue;
			m.header.size = dataFromQueue.size();
			m.send(s);
			messages.pop();
		}

	}
};
#endif
