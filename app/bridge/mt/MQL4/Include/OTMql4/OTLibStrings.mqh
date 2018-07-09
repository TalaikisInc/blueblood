// -*-mode: c; c-style: stroustrup; c-basic-offset: 4; coding: utf-8-dos -*-

/*
 Miscellaneous functions that help handling strings.

 This includes Ansi to Unicode "issues".

*/

#property copyright "Copyright 2015, OpenTrading"
#property link      "https://github.com/OpenTrading/"

#import "OTMql4/OTLibStrings.ex4"

string uAnsi2Unicode(int ptrStringMemory);
void vStringToArray(string uInput, string& uOutput[], string uDelim);
string uStringReplace(string uHaystack, string uNeedle, string uReplace);
#import
