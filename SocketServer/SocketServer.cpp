// SocketServer.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "pch.h"
#include "framework.h"
#include "SocketServer.h"


#ifdef _DEBUG
#define new DEBUG_NEW
#endif

SocketServer::SocketServer()
{

}

long long SocketServer::GetTimeData()
{
	return std::time(nullptr);
}

void SocketServer::ProcessClient(SOCKET hSock, Server* server)
{
	CSocket s;
	s.Attach(hSock);

	Message m;
	int code = m.receive(s); //return header.type

	cout << m.header.to << ": " << m.header.from << ": " << m.header.type << ": " << code << endl;

	auto iSessionFrom = server->sessions.find(m.header.from);
	if (iSessionFrom != server->sessions.end())
	{
		if (iSessionFrom->second->isConnected == false && code != MT_INIT && code != MT_GETDATA && code != MT_EXIT)
		{
			return;
		}
	}

	switch (code)
	{
	case MT_INIT:
	{
		auto session = make_shared<Session>(++server->maxID, m.data);
		server->sessions[session->id] = session;
		session->lastInteractionTime = GetTimeData();
		session->isConnected = true;
		string answerFromServer;
		answerFromServer = "Hello, " + m.data + '\n' + "You was connected" + '\n' + "Your ID: " + to_string(session->id)+'\n';
		
		Message::send(s, session->id, MR_BROKER, MT_INIT, answerFromServer);
		break;
	}
	case MT_EXIT:
	{
		server->sessions.erase(m.header.from);
		Message::send(s, m.header.from, MR_BROKER, MT_CONFIRM,"");
		cout << "User was disconnected" << endl;
		Sleep(500);
		return;
	}
	case MT_GETDATA:
	{
		auto iSession = server->sessions.find(m.header.from);
		if (iSession != server->sessions.end())
		{
			iSession->second->send(s);
		}
		break;
	}
	case MT_DISCONNECT_USER:
	{
		server->sessions.erase(m.header.from);
		Message::send(s, m.header.from, MR_BROKER, MT_CONFIRM, "You was disconnected, timeout");
		cout << "User was disconnected" << endl;
		Sleep(500);
		return;
	}
	default:
	{
		if (m.header.to == MR_ALL)
		{
			for (auto& [id, session] : server->sessions)
			{
				if (id != m.header.from)
					session->add(m);
			}
		} else
		{ 
		auto iSessionFrom = server->sessions.find(m.header.from);
		if (iSessionFrom != server->sessions.end())
		{
			auto iSessionTo = server->sessions.find(m.header.to);
			if (iSessionTo != server->sessions.end())
			{
				iSessionTo->second->add(m);
			}
			else
			{
				Message response(m.header.from, MR_BROKER, MT_NOTUSER);
				iSessionFrom->second->add(response);
			}
		}
		}
		break;
	}
	}
	if (code != MT_GETDATA && code != MT_INIT)
	{
		auto SessionFrom = server->sessions.find(m.header.from);
		if (SessionFrom != server->sessions.end())
		{
			SessionFrom->second->lastInteractionTime = GetTimeData();
			//cout << SessionFrom->second->id << " Last interactin time changed: " << SessionFrom->second->lastInteractionTime;
		}
	}
}


CWinApp theApp;

int main()
{
	int nRetCode = 0;

	HMODULE hModule = ::GetModuleHandle(nullptr);

	if (hModule != nullptr)
	{
		// initialize MFC and print and error on failure
		if (!AfxWinInit(hModule, nullptr, ::GetCommandLine(), 0))
		{
			// TODO: code your application's behavior here.
			wprintf(L"Fatal Error: MFC initialization failed\n");
			nRetCode = 1;
		}
		else
		{
			Server server;
		}
	}
	else
	{
		// TODO: change error code to suit your needs
		wprintf(L"Fatal Error: GetModuleHandle failed\n");
		nRetCode = 1;
	}

	return nRetCode;
}
