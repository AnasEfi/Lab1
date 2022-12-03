// SocketClient.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "pch.h"
#include "framework.h"
#include "../SocketServer/Message.h"
#include <iostream>
#include <string>
#include "Client.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

using namespace std;

void ProcessMessages(Client NewClient)
{
	while (true)
	{
		Sleep(1000);
		Message m = NewClient.send(MR_BROKER, MT_GETDATA,"");
		switch (m.header.type)
		{
		case MT_DATA:
			cout << m.data << endl;
			break;
		case MT_NOTUSER:
			cout << "User not found " << endl;
			break;
		case MT_DISCONNECT_USER:
		{
			cout << "Timeout, you was disconnected" << endl;
			Message m = NewClient.send(MR_BROKER, MT_EXIT,"");
			NewClient.isConnected = true;
			Sleep(1000);
			return;
		}
		default:
			Sleep(100);
			break;
		}
	}
}

void ConnectClient(Client NewClient)
{
	AfxSocketInit();
	string name;
	getline(cin, name);
	Message m = NewClient.send(MR_BROKER, MT_INIT, name);

	if (m.header.type == MT_INIT)
	{
		cout << m.data << endl;
	}
	
	thread t(ProcessMessages,NewClient);
	t.detach();

	while (true)
	{
		string str, command;
		getline(cin, str);//ïðîâåðêà íà npos

		// ÏÐÎÂÅÐÈÒÜ, ×ÒÎ ÔËÀÆÎÊ ÏÎÄÊËÞ×ÅÍÈß Â TRUE
		if (NewClient.isConnected)
			return;
		command = str.substr(0, str.find_first_of(' '));//ïîèñê êîìàíäû â ñîîáùåíèè ïîëüçîâàòåëÿ

		if (command == "exit")
		{
			Message m = NewClient.send(MR_BROKER, MT_EXIT,"");
			if (m.header.type == MT_CONFIRM)
			{
				cout << "You are disconected" << endl;
				Sleep(1000);
				return;
			}
		}
		else if (command == "All")
		{
			string data = str.substr(str.find_first_of(' ') + 1, str.size() - 1);
			NewClient.send(MR_ALL, MT_DATA, data);
		}
		else if (command == "Send")
		{
			int to = stoi(str.substr(str.find_first_of(' ') + 1, str.find_first_of(' ')));
			if (to == NewClient.clientID)
			{
				cout << "You can't send message to yourself" << endl;
			}
			else
			{
				string subdata = str.substr(str.find_first_of(' ') + 1, str.size() - 1);
				string data = subdata.substr(subdata.find_first_of(' ') + 1, str.size() - 1);
				NewClient.send(to, MT_DATA, data);
			}
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
			Client client;
			ConnectClient(client);
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
