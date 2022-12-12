#ifndef SERVER_H
#define SERVER_H


#include "Session.h"
#include "Message.h"
#include "SocketServer.h"


class Server
{
public:
	static const long long TIMEOUT = 3000;
	int maxID = MR_USER;
	int storageID = 0;
	map<int, shared_ptr<Session>> sessions;
	//map<int, shared_ptr<Session>> storage_sessions;
	void CheckLastInteraction();
	
	Server();
};

#endif
