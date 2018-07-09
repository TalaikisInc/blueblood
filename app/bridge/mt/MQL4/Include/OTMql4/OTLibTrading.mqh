// -*-mode: c; c-style: stroustrup; c-basic-offset: 4; coding: utf-8-dos -*-

#property copyright "Copyright 2013 OpenTrading"
#property link      "https://github.com/OpenTrading/"

#import "OTMql4/OTLibTrading.ex4"

int iOTOrderSelect(int iIndex, int iSelect, int iPool);
int iOTOrderSendMarket(string sSymbol, int cmd, double fVolume,
                       int iStops=3, int iProfits=10, int slippage=3);
int iOTOrderSend(string sSymbol, int cmd,
                 double volume, double price, int slippage,
                 double stoploss, double takeprofit,
                 string comment="", int magic=0, datetime expiration=0,
                 color arrow_color=CLR_NONE);
int iOTOrderCloseMarket(int iTicket, int iSlippage=3, color cColor=CLR_NONE);
int iOTOrderCloseFull(int iTicket, double fPrice, int iSlippage=3, color cColor=CLR_NONE);
int iOTOrderClose(int iTicket,  double fLots, double fPrice, int iSlippage, color cColor=CLR_NONE);

int iOTSetTradeIsBusy(int iMaxWaitingSeconds);
int iOTSetTradeIsNotBusy();

double fOTExposedEcuInMarket(int iOrderEAMagic);
bool bOTIsTradeAllowed();
int iOTRefreshRates();
int iOTMarketInfo(string s, int iMode);
double fOTMarketInfo(string s, int iMode);
bool bOTModifyTrailingStopLoss(string sSymbol, int iTrailingStopLossPoints,
                               datetime tExpiration);
bool bOTModifyOrder(string sMsg,
                  int iTicket,
                  double fPrice,
                  double fStopLoss,
                  double fTakeProfit,
                  datetime tExpiration);
bool bOTContinueOnOrderError(int iTicket);
