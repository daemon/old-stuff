#include <windows.h>

class ConsoleWindow
{
      WORD *colors;
      HANDLE hdout; 
      int colorIndex;
      char *title;
      public:
             ConsoleWindow(HANDLE, int);
             void setColor(int);
             void setTitle(char*);
             
};
