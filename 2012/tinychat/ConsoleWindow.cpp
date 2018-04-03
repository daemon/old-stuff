#include "ConsoleWindow.h"
#include <stdio.h>
#include <windows.h>

ConsoleWindow::ConsoleWindow(HANDLE hdout, int colorIndex)
{
    this->hdout = hdout;
    this->colors = colors;
    setColor(colorIndex);
}

void ConsoleWindow::setColor(int colorIndex)
{
    SetConsoleTextAttribute(hdout, (WORD)colorIndex);
}

void ConsoleWindow::setTitle(char* title)
{
    this->title = title;
    SetConsoleTitleA((LPCSTR)title);
    
}

