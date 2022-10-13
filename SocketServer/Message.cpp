#include "pch.h"
#include "Message.h"

string GetLastErrorString(DWORD ErrorID = 0)
{
	if (!ErrorID)
		ErrorID = GetLastError();
	if (!ErrorID)
		return string();

	LPSTR pBuff = nullptr;
	size_t size = FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS,
		NULL, ErrorID, MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT), (LPSTR)&pBuff, 0, NULL);
	string s(pBuff, size);
	LocalFree(pBuff);

	return s;
}

int Message::clientID = 0;

int Message::Receive(CSocket& s, Message& resultMessage)
{
	if (!s.Receive(&resultMessage.header, sizeof(MessageHeader)))
		resultMessage.header.type = MT_NODATA;

	if (resultMessage.header.size)
	{
		vector <char> v(resultMessage.header.size);
		s.Receive(&v[0], (int)resultMessage.header.size); //return the amount of getting bites
		resultMessage.data = string(&v[0], resultMessage.header.size);
	}

	return resultMessage.header.type;
}

void Message::send(CSocket& s, int to, int from, int type, const string& data)
{
	Message m(to, from, type, data);
	m.send(s);
}

Message Message::send(int to, int type, const string& data)
{
	CSocket s;
	s.Create();
	if (!s.Connect("127.0.0.1", 12345))
	{
		throw runtime_error(GetLastErrorString());
	}
	Message m(to, clientID, type, data);
	m.send(s);
	if (m.receive(s) == MT_INIT)
	{
		clientID = m.header.to;
	}
	return m;
}

