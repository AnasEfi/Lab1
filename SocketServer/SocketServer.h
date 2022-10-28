#ifndef SOCKET_SERVER_H
#define SOCKET_SERVER_H


#include "resource.h"
#include "Server.h"
#include "Message.h"
#include "Session.h"

class Server;
class SocketServer
{
public:
	SocketServer();
	void ProcessClient(SOCKET hSock, Server* server);
	static long long GetTimeData();
};
#endif // !SOCKET_SERVER_H
