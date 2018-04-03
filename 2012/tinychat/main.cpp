#include <cstdlib>
#include "Connection.h"
#include "ConsoleWindow.h"
#include "StringTools.h"

using namespace std;

int main(int argc, char *argv[])
{
    char *user = argv[1];
    char *pass = argv[2];
    
    ConsoleWindow cnsWnd(GetStdHandle(STD_OUTPUT_HANDLE), 0);
    cnsWnd.setTitle("TinyChat");
    cnsWnd.setColor(7);
    
    Connection conn("208.122.59.226", 5005, user, pass);
    printf("Connecting...\n");
    conn.connectToServer();   
    char messages[32][64];
    char colors[32];
    while (true)
    {
        memset(messages, 0, sizeof(messages));
        memset(colors, 7, sizeof(colors));
        conn.recvIntoBuffer();
        conn.parseBuffer(messages, colors);
        for (int i = 0; i < 32; i++)
        {
            if (messages[i][0] == 0)
            {
                break;
            }
            cnsWnd.setColor((int)colors[i]);
            printf("%s\n", messages[i]);
        }
    }
    conn.closeSocket();
    return EXIT_SUCCESS;
}
