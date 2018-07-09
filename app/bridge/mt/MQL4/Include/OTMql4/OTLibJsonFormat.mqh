// -*-mode: c; c-style: stroustrup; c-basic-offset: 4; coding: utf-8-dos -*-

#property copyright "Copyright 2013 OpenTrading"
#property link      "https://github.com/OpenTrading/"

#import "OTMql4/OTLibJsonFormat.ex4"

string jOTAccountInformation();
string jOTOrdersTickets();
string jOTOrdersTrades();
string jOTOrdersHistory();
string jOTOrders(int iMode);
string jOTOrderInformationByTicket(int iTicket);
string jOTMarketInformation(string uSymbol);
string jOTTickInformation(string uSymbol, int iTimeFrame);
string jOTBarInformation(string uSymbol, int iTimeFrame, int iBar);
string jOTTimerInformation();
#import