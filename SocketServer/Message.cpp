#include "pch.h"
#include "Message.h"



void Message::send(CSocket& s, int to, int from, int type, const string& data)
{
	Message m(to, from, type, data);
	m.send(s);
}



