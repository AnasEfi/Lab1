#ifndef SERVER_H
#define SERVER_H


#include "Session.h"
#include "Message.h"
#include "SocketServer.h"


class Server
{
public:
	static const long long TIMEOUT = 30;
	int maxID = MR_USER;
	map<int, shared_ptr<Session>> sessions;
	void CheckLastInteraction();
	Server();
};

#endif
