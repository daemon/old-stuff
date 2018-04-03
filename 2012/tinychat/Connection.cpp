#include "Connection.h"
#include "StringTools.h"

Connection::Connection(char* host_ip, int port, char* user, char* pass)
{
     this->host_ip = host_ip;
     this->port = port;
     this->user = user;
     this->pass = pass;
     this->MSGPUB = "MSG:PUB:";
     memset(MSGBUFFER, 0, sizeof(MSGBUFFER));
}

int Connection::connectToServer()
{
     WORD sockV;
     WSADATA wsaData;
     sockV = MAKEWORD(1, 1);
     WSAStartup(sockV, &wsaData);
     
     sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    
     //LPHOSTENT host;
     //unsigned long address = inet_addr(host_ip);
     //host = gethostbyaddr((char*)&address, sizeof(address), AF_INET);
          
     SOCKADDR_IN server;
     memset(&server, 0, sizeof(server));
     server.sin_family = AF_INET;
     server.sin_addr.s_addr = inet_addr(host_ip);
     server.sin_port = htons(port);
     
     short res = connect(sock, (struct sockaddr *)&server, sizeof(server));
     Sleep(2000);
     char *buffer = new char[128];
     ZeroMemory(buffer, 128);
     strcpy(buffer, "LOGIN:TinyChat:");
     strcat(buffer, user);
     strcat(buffer, ":");
     strcat(buffer, pass);
     strcat(buffer, "\n");
     send(sock, buffer, strlen(buffer), 0);
     Sleep(2000);
     delete buffer;
     this->arena_change("");
     return 0;
}

void Connection::closeSocket()
{
     closesocket(sock);
     WSACleanup();
}

int Connection::send_priv(char* user, char* msg)
{
     char * buffer = new char[128];
     ZeroMemory(buffer, 128);
     strcpy(buffer, "SEND:PRIV:");
     strcat(buffer, user);
     strcat(buffer, ":");
     strcat(buffer, msg);
     strcat(buffer, "\n");
     send(sock, buffer, strlen(buffer), 0);
     delete buffer;
     return 0;
}

int Connection::send_pub(char* msg)
{
     char * buffer = new char[128];
     ZeroMemory(buffer, 128);
     strcpy(buffer, "SEND:PUB:");
     strcat(buffer, msg);
     strcat(buffer, "\n");
     send(sock, buffer, strlen(buffer), 0);
     delete buffer;
     return 0;
}

int Connection::send_chat(char *chan, char* msg)
{
     char * buffer = new char[128];
     ZeroMemory(buffer, 128);
     strcpy(buffer, "SEND:CHAT:");
     strcat(buffer, chan);
     strcat(buffer, ";");
     strcat(buffer, msg);
     strcat(buffer, "\n");
     send(sock, buffer, strlen(buffer), 0);
     delete buffer;
     return 0;
}

int Connection::send_cmd(char* msg)
{
     char * buffer = new char[128];
     ZeroMemory(buffer, 128);
     strcpy(buffer, "SEND:CMD:");
     strcat(buffer, msg);
     strcat(buffer, "\n");
     send(sock, buffer, strlen(buffer), 0);
     delete buffer;
     return 0;
}

int Connection::send_cmd(char *user, char* msg)
{
     char * buffer = new char[128];
     ZeroMemory(buffer, 128);
     strcpy(buffer, "SEND:PRIVCMD:");
     strcat(buffer, user);
     strcat(buffer, ":");
     strcat(buffer, msg);
     strcat(buffer, "\n");
     send(sock, buffer, strlen(buffer), 0);
     delete buffer;
     return 0;
}

int Connection::arena_change(char* arena)
{
     char *buffer = new char[128];
     ZeroMemory(buffer, 128);
     strcpy(buffer, "GO:");
     strcat(buffer, arena);
     strcat(buffer, "\n");                               
     send(sock, buffer, sizeof(buffer), 0);
     delete buffer;
     return 0;
}

void Connection::parseBuffer(char messages[32][64], char colors[])
{
     memset(newlinesList, 0, sizeof(newlinesList));  
     getNewLinesIndex(MSGBUFFER, newlinesList);
     short i = 0, prevIndex = 0;
     
     while (newlinesList[i] != 0)
     {
          if (prevIndex != 0)
              prevIndex++;
           short position = prevIndex;          
           char *tmp;
           
           tmp = MSGBUFFER + prevIndex;
           while (*tmp != '\n')
                 *tmp++ = MSGBUFFER[prevIndex++]; 
           *tmp = '\0';
           tmp -= (prevIndex - position);
           
           if (prevIndex - position > 8 && startsWith(tmp, MSGPUB))
              colors[i] = 3;
               
           
           
           strcpy(messages[i], tmp);
           
           delete tmp;
           i++;
     }
     memset(MSGBUFFER, 0, sizeof(MSGBUFFER));
     return;
}

void Connection::recvIntoBuffer(void)
{
     recv(sock, MSGBUFFER, sizeof(MSGBUFFER), 0);
}

void Connection::getNewLinesIndex(char* ptr, int listOfLines[])
{
     short counter = 0;
     for (int i = 0; i < 1024; i++)
     {
         if (ptr[i] == '\n')
         {
              listOfLines[counter] = i;
              counter++;
         } else if (ptr[i] == 0)
              return;         
     }
}

