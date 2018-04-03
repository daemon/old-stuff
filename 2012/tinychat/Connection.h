#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

class Connection
{
      char *host_ip, *user, *pass, *MSGPUB;
      int port;
      int newlinesList[32];
      SOCKET sock;
      char MSGBUFFER[512];
      public:
             Connection (char*, int, char*, char*);
             int connectToServer(void);
             int arena_change(char*);
             int send_priv(char*, char*);
             int send_cmd(char*);
             int send_cmd(char*, char*);
             int send_pub(char*);
             int send_chat(char*, char*);
             void closeSocket(void);
             void recvIntoBuffer(void);
             void parseBuffer(char[32][64], char[]);
      private:
              void getNewLinesIndex(char*, int[]);
};
