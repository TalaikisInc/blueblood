// -*-mode: c; c-style: stroustrup; c-basic-offset: 4; coding: utf-8-dos -*-

//  This is the replacement for what should be Eval in Mt4:
//  take a string expression and evaluate it.
//
//  We know this is verbose and could be done more compactly,
//  but it's clean and robust so we'll leave it like this for now.
//
//  If you want to extend this for your own functions you have declared in Mql4,
//  look at how zOTLibProcessCmd calls zMt4LibProcessCmd and then
//  goes on and handles it if zMt4LibProcessCmd didn't.
//

#property copyright "Copyright 2013 OpenTrading"
#property link      "https://github.com/OpenTrading/"
#property library

#include <stdlib.mqh>
#include <stderror.mqh>
#include <OTMql4/OTLibLog.mqh>
#include <OTMql4/OTLibStrings.mqh>
#include <OTMql4/OTLibSimpleFormatCmd.mqh>
#include <OTMql4/OTLibMt4ProcessCmd.mqh>
// extentions from OpenTrading - see uProcessCmdgOT and uProcessCmdOT
#include <OTMql4/OTLibJsonFormat.mqh>
#include <OTMql4/OTLibTrading.mqh>

string zOTLibProcessCmd(string uMess) {
    //  This is the replacement for what should be Eval in Mt4:
    //  take a string expression and evaluate it.
    //  zMt4LibProcessCmd handles base Mt4 expressions, and
    //  zOTLibProcessCmd also handles base OpenTrading expressions.

    //  Returns the result of processing the command.
    //  Returns "" if there is an error.

    string uType, uChartId, uIgnore, uMark, uCmd;
    string uArg1="";
    string uArg2="";
    string uArg3="";
    string uArg4="";
    string uArg5="";
    string uArg6="";
    string uArg7="";
    string aArrayAsList[];
    int iLen;
    string uRetval, uKey;

    iLen =  StringLen(uMess);
    if (iLen <= 0) {return("");}

    uRetval = zOTLibMt4ProcessCmd(uMess);
    if (uRetval != "") {
        //vTrace("zOTLibProcessCmd: returning " +uRetval);
        return(uRetval);
    }

    vStringToArray(uMess, aArrayAsList, "|");

    iLen = ArraySize(aArrayAsList);
    // vTrace("zOTLibProcessCmd: " +uMess +" ArrayLen " +iLen);

    uRetval = eOTLibSimpleUnformatCmd(aArrayAsList);
    if (uRetval != "") {
        vError("eOTLibProcessCmd: preprocess failed with error: " +uRetval);
        return("");
    }

    uType   = aArrayAsList[0];
    uChartId  = aArrayAsList[1];
    uIgnore = aArrayAsList[2];
    uMark   = aArrayAsList[3];
    uCmd    = aArrayAsList[4];
    uArg1   = aArrayAsList[5];
    uArg2   = aArrayAsList[6];
    uArg3   = aArrayAsList[7];
    uArg4   = aArrayAsList[8];
    uArg5   = aArrayAsList[9];
    uArg6   = aArrayAsList[10];
    uArg7   = aArrayAsList[11];

    uKey = StringSubstr(uCmd, 0, 3);
    if (uKey == "gOT") {
        // extentions from OpenTrading
        uRetval = uProcessCmdgOT(uCmd, uChartId, uIgnore, uMark, uArg1, uArg2, uArg3, uArg4, uArg5, uArg6, uArg7);

        if (StringCompare(uRetval, "") == 0 ) vDebug("zOTLibProcessCmd: UNHANDELED gOT uCmd: " +uCmd);
    } else if (StringSubstr(uCmd, 1, 2) == "OT") {
        uRetval = uProcessCmdOT(uCmd, uChartId, uIgnore, uMark, uArg1, uArg2, uArg3, uArg4, uArg5, uArg6, uArg7);
        if (StringCompare(uRetval, "") == 0 ) vDebug("zOTLibProcessCmd: UNHANDELED OT uCmd: " +uCmd);

    } else if (StringSubstr(uCmd, 0, 1) == "i") {
        //? are these Mt4 or OT?
        uRetval = uProcessCmdi(uCmd, uChartId, uIgnore, uMark, uArg1, uArg2, uArg3, uArg4, uArg5, uArg6, uArg7);
        if (StringCompare(uRetval, "") == 0 ) vDebug("zOTLibProcessCmd: UNHANDELED i uCmd: " +uCmd);

    }
    if (StringCompare(uRetval, "") == 0) {
        //vTrace("zOTLibProcessCmd: UNHANDELED uCmd: " +uCmd);
        return("");
    }
    // vTrace("zOTLibProcessCmd uMess: " +uMess +" -> " +uRetval);

    // WE INCLUDE THE SMARK
    uRetval = uMark + "|" + uRetval;
    return(uRetval);

}

string uProcessCmdi (string uCmd, string uChartId, string uIgnore, string uMark, string uArg1, string uArg2, string uArg3, string uArg4, string uArg5, string uArg6, string uArg7) {
    string uMsg;
    string uRetval="none|";
    string uSymbol;
    int iPeriod, iShift;
    int iType, iCount, iStart;

    if (StringFind(uCmd, "|", 0) >= 0) {
        uMsg="found separator in command";
        vWarn(uMsg +": " +uCmd);
        uRetval=uMark +"|error|"+uMsg;
        return(uRetval);
    }

    uSymbol = uArg1;
    iPeriod = StrToInteger(uArg2);

    // iBarShift
    if (uCmd == "iBars") {
        uRetval = "int|" +IntegerToString( iBars(uSymbol, iPeriod));
    } else if (uCmd == "iClose") {
        iShift = StrToInteger(uArg3);
        uRetval = "double|" +DoubleToStr( iClose(uSymbol, iPeriod, iShift), 4);
    } else if (uCmd == "iHigh") {
        iShift = StrToInteger(uArg3);
        uRetval = "double|" +DoubleToStr( iHigh(uSymbol, iPeriod, iShift), 4);
    } else if (uCmd == "iHighest") {
        iType = StrToInteger(uArg3);
        iCount = StrToInteger(uArg4);
        iStart = StrToInteger(uArg5);
        uRetval = "int|" +IntegerToString( iHighest(uSymbol, iPeriod, iType, iCount, iStart));
    } else if (uCmd == "iLow") {
        iShift=StrToInteger(uArg3);
        uRetval = "double|" +DoubleToStr( iLow(uSymbol, iPeriod, iShift), 4);
    } else if (uCmd == "iLowest") {
        iType = StrToInteger(uArg3);
        iCount = StrToInteger(uArg4);
        iStart = StrToInteger(uArg5);
        uRetval = "int|" +IntegerToString( iLowest(uSymbol, iPeriod, iType, iCount, iStart));
    } else if (uCmd == "iOpen") {
        iShift = StrToInteger(uArg3);
        uRetval = "double|" +DoubleToStr( iOpen(uSymbol, iPeriod, iShift), 4);
    } else if (uCmd == "iTime") {
        iShift = StrToInteger(uArg3);
        uRetval = "datetime|" + iTime(uSymbol, iPeriod, iShift);
    } else if (uCmd == "iVolume") {
        iShift = StrToInteger(uArg3);
        uRetval = "double|" +DoubleToStr( iVolume(uSymbol, iPeriod, iShift), 2);
    } else {
        uMsg="Unrecognized action: ";
        vWarn(uMsg + uCmd);
        uRetval=uMark +"|error|"+uMsg;
    }

    return(uRetval);
}

// OpenTrading additions
// names start with a lower case letter then OT
string uProcessCmdOT(string uCmd, string uChartId, string uIgnore, string uMark, string uArg1, string uArg2, string uArg3, string uArg4, string uArg5, string uArg6, string uArg7) {
    string uMsg, sSymbol;
    string uRetval="none|";
    int iTicket, iTimeframe, iCmd, iBar;
    double fLots;
    double fPrice;
    double fStopLoss;
    double fTakeProfit;
    datetime tExpiration;
    int iMaxWaitingSeconds;
    int iOrderEAMagic;
    int iTrailingStopLossPoints;
    int iSlippage;
    color cColor;

    if (StringFind(uCmd, "|", 0) >= 0) {
        uMsg="Found separator in command";
        vWarn(uMsg + uCmd);
        uRetval=uMark +"|error|"+uMsg;
        return(uRetval);
    }

    if (uCmd == "iOTOrderSelect") {
        uRetval = "int|" +IntegerToString( iOTOrderSelect(StrToInteger(uArg1), StrToInteger(uArg2), StrToInteger(uArg3)));

    } else if (uCmd == "iOTOrderSend") {
        sSymbol = uArg1;
        // assert string length > 3
        iCmd = StrToInteger(uArg2);
        fLots = StrToDouble(uArg3);
        fPrice = StrToDouble(uArg4);
        iSlippage = StrToInteger(uArg5);
        fStopLoss = StrToDouble(uArg6);
        fTakeProfit = StrToDouble(uArg7);
        // FixMe:
        cColor=CLR_NONE;
        uRetval = "int|" +IntegerToString(iOTOrderSend(sSymbol, iCmd,
                                                       fLots, fPrice, iSlippage,
                                                       fStopLoss, fTakeProfit
                                                       ));

    } else if (uCmd == "iOTOrderSendMarket") {
        sSymbol = uArg1;
        iCmd = StrToInteger(uArg2);
        fLots = StrToDouble(uArg3);
        // fPrice = StrToDouble(uArg4);
        // iSlippage = StrToInteger(uArg5);
        // FixMe:
        cColor=CLR_NONE;
        uRetval = "int|" +IntegerToString( iOTOrderSendMarket(sSymbol, iCmd, fLots));

    } else if (uCmd == "iOTOrderCloseMarket") {
        iTicket = StrToInteger(uArg1);
        uRetval = "int|" +IntegerToString( iOTOrderCloseMarket(iTicket));

    } else if (uCmd == "iOTOrderCloseFull") {
        iTicket = StrToInteger(uArg1);
        fLots = StrToDouble(uArg2);
        fPrice = StrToDouble(uArg3);
        // FixMe:
        iSlippage = StrToInteger(uArg4);
        // FixMe:
        cColor=CLR_NONE;
        uRetval = "int|" +IntegerToString( iOTOrderCloseFull(iTicket, fPrice, iSlippage, cColor));

    } else if (uCmd == "iOTOrderClose") {
        iTicket = StrToInteger(uArg1);
        fLots = StrToDouble(uArg2);
        fPrice = StrToDouble(uArg3);
        iSlippage = StrToInteger(uArg4);
        // FixMe:
        cColor=CLR_NONE;
        uRetval = "int|" +IntegerToString( iOTOrderClose(iTicket, fLots, fPrice, iSlippage, cColor));

    } else if (uCmd == "iOTSetTradeIsBusy") {
        if (StringLen(uArg1) < 1) {
            uRetval = "int|" +IntegerToString( iOTSetTradeIsBusy(60));
        } else {
            iMaxWaitingSeconds = StrToInteger(uArg1);
            uRetval = "int|" +IntegerToString( iOTSetTradeIsBusy(iMaxWaitingSeconds));
        }

    } else if (uCmd == "iOTSetTradeIsNotBusy") {
        uRetval = "int|" +IntegerToString( iOTSetTradeIsNotBusy());

    } else if (uCmd == "fOTExposedEcuInMarket") {
        if (StringLen(uArg1) < 1) {
            iOrderEAMagic = 0;
        } else {
            iOrderEAMagic = StrToInteger(uArg1);
        }
        uRetval = "double|" +DoubleToStr( fOTExposedEcuInMarket(iOrderEAMagic), 2);

    } else if (uCmd == "bOTIsTradeAllowed") {
        uRetval = "bool|" + bOTIsTradeAllowed();

    } else if (uCmd == "iOTRefreshRates") {
        uRetval = "bool|" + iOTRefreshRates();

    } else if (uCmd == "iOTMarketInfo") {
        sSymbol = uArg1;
        iCmd = StrToInteger(uArg2);
        uRetval = "int|" + iOTMarketInfo(sSymbol, iCmd);

    } else if (uCmd == "fOTMarketInfo") {
        sSymbol = uArg1;
        iCmd = StrToInteger(uArg2);
        uRetval = "double|" + fOTMarketInfo(sSymbol, iCmd);

    } else if (uCmd == "bOTModifyTrailingStopLoss") {
        sSymbol = uArg1;
        iTrailingStopLossPoints = StrToInteger(uArg2);
        if (StringLen(uArg3) < 1) {
            tExpiration = 0;
        } else {
            // FixMe: StrToDateTime?
            tExpiration = StrToInteger(uArg3);
        }
        uRetval = "bool|" + bOTModifyTrailingStopLoss(sSymbol,
                                                      iTrailingStopLossPoints,
                                                      tExpiration);

    } else if (uCmd == "bOTModifyOrder") {
        // this implies a selected order
        iTicket = StrToInteger(uArg2);
        fPrice = StrToDouble(uArg3);
        fStopLoss = StrToDouble(uArg4);
        fTakeProfit = StrToDouble(uArg5);
        // ignores datetime tExpiration
        tExpiration = 0;
        // Notes: Open price and expiration time can be changed only for pending orders.
        uRetval = "bool|" + bOTModifyOrder(uArg1, iTicket, fPrice,
                                           fStopLoss, fTakeProfit, tExpiration);

    } else if (uCmd == "bOTContinueOnOrderError") {
        iTicket = StrToInteger(uArg1);
        uRetval = "bool|" + bOTContinueOnOrderError(iTicket);

    } else if (uCmd == "jOTAccountInformation") {
        uRetval = "json|" + jOTAccountInformation();
    } else if (uCmd == "jOTOrdersTickets") {
        uRetval = "json|" + jOTOrdersTickets();
    } else if (uCmd == "jOTOrdersHistory") {
        uRetval = "json|" + jOTOrdersHistory();
    } else if (uCmd == "jOTOrdersTrades") {
        uRetval = "json|" + jOTOrdersTrades();
    } else if (uCmd == "jOTOrders") {
        uRetval = "json|" + jOTOrders(StrToInteger(uArg1));
    } else if (uCmd == "jOTOrderInformationByTicket") {
        iTicket = StrToInteger(uArg1);
        uRetval = "json|" + jOTOrderInformationByTicket(iTicket);
    } else if (uCmd == "jOTMarketInformation") {
        uRetval = "json|" + jOTMarketInformation(uArg1);
    } else if (uCmd == "jOTBarInformation") {
        iTimeframe = StrToInteger(uArg2);
        iBar = StrToInteger(uArg3);
        uRetval = "json|" + jOTBarInformation(uArg1, iTimeframe, iBar);
    } else {
        uMsg = "Unrecognized action: ";
        vWarn("uProcessCmdOT: " +uMsg +uCmd);
        uRetval = "";
    }

    return(uRetval);
}


// Wrap all of the functions that depend on an order being selected
// into a generic gOTWithOrderSelectByTicket and gOTWithOrderSelectByPosition
string uProcessCmdgOT(string uCmd, string uChartId, string uIgnore, string uMark, string uArg1, string uArg2, string uArg3, string uArg4, string uArg5, string uArg6, string uArg7) {
    string uRetval="none|";
    string uMsg;
    int iError;

    if (StringFind(uCmd, "|", 0) >= 0) {
        uMsg="Found separator in command";
        vWarn(uMsg + uCmd);
        uRetval=uMark +"|error|"+uMsg;
        return(uRetval);
    }

    if (uCmd == "gOTWithOrderSelectByTicket") {
        int iTicket=StrToInteger(uArg1);

        if (OrderSelect(iTicket, SELECT_BY_TICKET) == false) {
            iError=GetLastError();
            uMsg = "OrderSelect returned an error: " + ErrorDescription(iError)+"("+iError+")";
            vError(uMsg);
            uRetval=uMark +"|error|"+uMsg;
            return(uRetval);
        }
        // drop through
    } else if (uCmd == "gOTWithOrderSelectByPosition") {
        int iPos=StrToInteger(uArg1);

        if (OrderSelect(iPos, SELECT_BY_POS) == false) {
            iError=GetLastError();
            uMsg = "OrderSelect returned an error: " + ErrorDescription(iError)+"("+iError+")";
            vError(uMsg);
            uRetval=uMark +"|error|"+uMsg;
            return(uRetval);
        }
        // drop through
    } else {
        uMsg="Unrecognized action";
        vWarn(uMsg + uCmd);
        uRetval=uMark +"|error|"+uMsg;
        return(uRetval);
    }

    string sCommand=uArg2;
    // have a selected order ...
    if (sCommand == "OrderClosePrice" ) {
        uRetval = "double|" +DoubleToStr( OrderClosePrice(), 4);
    } else if (sCommand == "OrderCloseTime" ) {
        uRetval = "datetime|" + OrderCloseTime();
    } else if (sCommand == "OrderComment" ) {
        uRetval = "string|" + OrderComment();
    } else if (sCommand == "OrderCommission" ) {
        uRetval = "double|" +DoubleToStr( OrderCommission(), 2);
    } else if (sCommand == "OrderExpiration" ) {
        uRetval = "datetime|" + OrderExpiration();
    } else if (sCommand == "OrderLots" ) {
        uRetval = "double|" +DoubleToStr( OrderLots(), 6);
    } else if (sCommand == "OrderMagicNumber" ) {
        uRetval = "int|" +IntegerToString( OrderMagicNumber());
    } else if (sCommand == "OrderOpenPrice" ) {
        uRetval = "double|" +DoubleToStr( OrderOpenPrice(), 4);
    } else if (sCommand == "OrderOpenTime" ) {
        uRetval = "datetime|" + OrderOpenTime();
    } else if (sCommand == "OrderProfit" ) {
        uRetval = "double|" +DoubleToStr( OrderProfit(), 2);
    } else if (sCommand == "OrderStopLoss" ) {
        uRetval = "double|" +DoubleToStr( OrderStopLoss(), 4);
    } else if (sCommand == "OrderSwap" ) {
        uRetval = "double|" +DoubleToStr( OrderSwap(), 4);
    } else if (sCommand == "OrderSymbol" ) {
        uRetval = "string|" + OrderSymbol();
    } else if (sCommand == "OrderTakeProfit" ) {
        uRetval = "double|" +DoubleToStr( OrderTakeProfit(), 4);
    } else if (sCommand == "OrderTicket" ) {
        uRetval = "int|" +IntegerToString( OrderTicket());
    } else if (sCommand == "OrderType" ) {
        uRetval = "int|" +IntegerToString( OrderType());
    } else {
        uMsg="Unrecognized " + uCmd + " command: " + sCommand;
        vWarn("uProcessCmdgOT: " +uMsg);
        uRetval="";
    }

    return(uRetval);
}

