// -*-mode: c; c-style: stroustrup; c-basic-offset: 4; coding: utf-8-dos -*-

/*
This is just a stub for a full logging system later.
*/
#property copyright "Copyright 2014 Open Trading"
#property link      "https://github.com/OpenTrading/"

#import "OTMql4/OTLibLog.ex4"

void vLogInit();
void vSetLogLevel(int i);
int iGetLogLevel();

void vLog(int iLevel, string sMsg);
void vError(string sMess);
void vWarn(string sMess);
void vInfo(string sMess);
void vDebug(string sMess);
void vTrace(string sMess);
#import
