#include "pch.h"
#include "Server.h"

Server::Server()
{
	
	AfxSocketInit();
	SocketServer ServerSocket = *(new SocketServer());
	CSocket Server;
	Server.Create(12345);

	thread checkConnection(&Server::CheckLastInteraction,this);
	checkConnection.detach();

	while (true)
	{
		if (!Server.Listen())
			break;

		CSocket s;
		Server.Accept(s);
		thread t(&SocketServer::ProcessClient, ServerSocket, s.Detach(), this);
		t.detach();
	}

}


void Server::CheckLastInteraction()
{
	while (true)
	{
		for (auto& [id, session] : sessions)
		{
			if (id != storageID)
			{
				if (session != nullptr &&
					SocketServer::GetTimeData() - session->lastInteractionTime > TIMEOUT && session->isConnected == true)
				{
					Message exitMsg(id, MR_BROKER, MT_DISCONNECT_USER);
					session->add(exitMsg);
					session->isConnected = false;
				}
			}
		}
		Sleep(3 * 1000);
	}
}