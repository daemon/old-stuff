#include "StringTools.h"


bool startsWith(char* string, char* substr, short len1, short len2)
{
     if (len2 > len1)
        return false;
     for (short index = 0; index < len2; index++)
          if (*(substr + index) != *(string + index))
               return false;
     
     return true;
}
