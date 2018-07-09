// -*-mode: c; c-style: stroustrup; c-basic-offset: 4; coding: utf-8-dos -*-

//  Miscellaneous functions that help handling strings.
//
//  This includes Ansi to Unicode "issues".
//

#property copyright "Copyright 2015, OpenTrading"
#property link      "https://github.com/OpenTrading/"
#property library

#import "kernel32.dll"
   int lstrlenA(int);
   void RtlMoveMemory(uchar & arr[], int, int);
   int LocalFree(int); // May need to be changed depending on how the DLL allocates memory
#import

//+----------------------------------------------------------------------------+
//| Lovely function that helps us to get ANSI strings from DLLs to our UNICODE |
//| format                                                                     |
//| http://forum.mql4.com/60708                                                |
//+----------------------------------------------------------------------------+
string uAnsi2Unicode(int iStringMemory) {
    int szString = lstrlenA(iStringMemory);
    uchar ucValue[];
    ArrayResize(ucValue, szString + 1);
    RtlMoveMemory(ucValue, iStringMemory, szString + 1);
    string uMessage = CharArrayToString(ucValue);
    // Free the string memory returned by the DLL.
    // This step can be removed but, without it, there will be a memory leak.
    // The correct method for freeing the string
    // *depends on how the DLL allocated the memory*
    // The following assumes that the DLL has used LocalAlloc
    // (or an indirect equivalent). If not,
    // then the following line may not fix the leak, and may even cause a crash.
    LocalFree(iStringMemory);
    return(uMessage);
}

void vStringToArray(string uInput, string& uOutput[], string uDelim) {
    int iStart=0;
    int iDelpos;
    string uNextelem;

    if (uInput == "") return;
    ArrayResize(uOutput, 0);

    while(iStart < StringLen(uInput)) {
        iDelpos = StringFind(uInput, uDelim, iStart);
        if(iDelpos < 0) {
            uNextelem = StringSubstr(uInput,iStart);
            iStart = StringLen(uInput);
        } else {
            uNextelem = StringSubstr(uInput, iStart, iDelpos-iStart);
            iStart = iDelpos+1;
        }
        ArrayResize(uOutput, ArraySize(uOutput)+1);
        uOutput[ArraySize(uOutput)-1] = uNextelem;
    }
}


string uStringReplace(string uHaystack, string uNeedle, string uReplace) {
    string left, right;
    int iStart=0;
    int rlen=StringLen(uReplace);
    int nlen=StringLen(uNeedle);

    while (iStart > -1) {
        iStart = StringFind(uHaystack, uNeedle, iStart);
        if (iStart > -1) {
            if(iStart > 0) {
                left = StringSubstr(uHaystack, 0, iStart);
            } else {
                left = "";
            }
            right = StringSubstr(uHaystack, iStart + nlen);
            uHaystack = left + uReplace + right;
            iStart = iStart + rlen;
        }
    }
    return (uHaystack);
}

