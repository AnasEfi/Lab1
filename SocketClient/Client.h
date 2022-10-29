#include <string>
#include "../SocketServer/Message.h"
#include <iostream>
#include <string>
#include "Resource.h"

using namespace std;

class Client
{
public:
	int clientID;
	string name;
	bool SUPER_FLAG_IS_DISCONNECTED = false;
	Message send(int to, int type, const string& data);
	Client();
};