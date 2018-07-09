// -*-mode: c; c-style: stroustrup; c-basic-offset: 4; coding: utf-8-dos -*-

// This is the replacement for what should be Eval in Mt4:
// take a string expression and evaluate it.
//
// We know this is verbose and could be done more compactly,
// but it's clean and robust so we'll leave it like this for now.
//
// If you want to extend this for your own functions you have declared in Mql4,
// look at how zOTLibProcessCmd calls zMt4LibProcessCmd in OTLibProcessCmd.mq4.

#property copyright "Copyright 2015 Open Trading"
#property link      "https://github.com/OpenTrading/"
#property library

#include <stdlib.mqh>
#include <stderror.mqh>
#include <OTMql4/OTLibLog.mqh>
#include <OTMql4/OTLibStrings.mqh>
#include <OTMql4/OTLibSimpleFormatCmd.mqh>

string zOTLibMt4ProcessCmd(string uMess) {
    //  This is the replacement for what should be Eval in Mt4:
    //  take a string expression and evaluate it.
    //  zMt4LibProcessCmd only handles base Mt4 expressions.

    //  Returns the result of processing the command as a string
    //  in the form "type|value" where type is one of:
    //  string, int, double, bool, datetime, void, json

    //  Returns "error|explanation" if there is an error.

    //  Returns "" if the the command was not recognized;
    //  you can use this fact to process the standard Mt4 commands
    //  with zOTLibMt4ProcessCmd,  and if it returns "",
    //  write your own zMyProcessCmd to process your additions.

    string uType, uChartId, uIgnore, uMark, uCmd, uMsg;
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
    if (iLen <= 0) {
        vError("eOTLibProcessCmd: empty input");
        return("");
    }

    vStringToArray(uMess, aArrayAsList, "|");

    iLen = ArraySize(aArrayAsList);
    //vTrace("zMt4LibProcessCmd: " +uMess +" ArrayLen " +iLen);

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

    if (StringFind(uCmd, "|", 0) >= 0) {
        uMsg="Found separator in command";
        vWarn(uMsg);
        uRetval=uMark+"|error|"+uMsg;
        return(uRetval);
    }

    if (uCmd == "OrdersTotal") { //0
        uRetval = "int|" +IntegerToString(OrdersTotal());
    } else if (uCmd == "Period") { //0
        uRetval = "int|" +IntegerToString(Period());
    } else if (uCmd == "RefreshRates") { //0
        uRetval = "bool|" +RefreshRates();
    } else if (uCmd == "Symbol") { //0
        uRetval = "string|" +Symbol();
    } else if (uCmd == "Comment") {
        // FixMe: what's the return value?
        Comment(uArg1);
        uRetval = "void|";
    } else if (uCmd == "Print") {
        // FixMe: what's the return value?
        // FixMe: we should handle multi-args
        Print(uArg1);
        uRetval = "void|";
    } else if (uKey == "Fil") {
        // FixMe: File*
        uRetval = "";
    } else if (uKey == "Ter") {
        uRetval = zProcessCmdTer(uCmd, uChartId, uIgnore, uArg1, uArg2, uArg3, uArg4, uArg5);
    } else if (uKey == "Win") {
        uRetval = zProcessCmdWin(uCmd, uChartId, uIgnore, uArg1, uArg2, uArg3, uArg4, uArg5);
    } else if (uKey == "Acc") {
        uRetval = zProcessCmdAcc(uCmd, uChartId, uIgnore, uArg1, uArg2, uArg3, uArg4, uArg5);
    } else if (uKey == "Glo") {
        uRetval = zProcessCmdGlo(uCmd, uChartId, uIgnore, uArg1, uArg2, uArg3, uArg4, uArg5);
    }

    if (StringCompare(uRetval, "") == 0) {
        //vTrace("zMt4LibProcessCmd: UNHANDELED" +uKey +" uCmd: " +uCmd);
        return("");
    }
    // vTrace("zMt4LibProcessCmd uMess: " +uMess +" -> " +uRetval);

    // WE INCLUDE THE SMARK
    uRetval = uMark + "|" + uRetval;

    return(uRetval);
}

string zProcessCmdTer(string uCmd, string uChartId, string uIgnore, string uArg1, string uArg2, string uArg3, string uArg4, string uArg5) {
    string uMsg;
    string uRetval="";

    if (uCmd == "TerminalCompany") { //0
        uRetval = "string|" +TerminalCompany();
    } else if (uCmd == "TerminalName") { //0
        uRetval = "string|" +TerminalName();
    } else if (uCmd == "TerminalInfoString") { //1
        // groan - does everything coerce?
        uRetval = "string|" +(string)TerminalInfoString(uArg1);
    } else if (uCmd == "TerminalPath") { //0
        uRetval = "string|" +TerminalPath();
    } else {
        uMsg = "Unrecognized action: ";
        vWarn("zProcessCmdTer: " +uMsg +uCmd);
        uRetval = "";
    }

    return (uRetval);
}

string zProcessCmdWin(string uCmd, string uChartId, string uIgnore, string uArg1, string uArg2, string uArg3, string uArg4, string uArg5) {
    string uMsg;
    string uRetval="";
    int iIndex, iPeriod;

    if (uCmd == "WindowBarsPerChart") { //0
        uRetval = "int|" +IntegerToString(WindowBarsPerChart());
    } else if (uCmd == "WindowFind") { //0
        uRetval = "string|" +WindowFind(uArg1);
    } else if (uCmd == "WindowFirstVisibleBar") { //0
        uRetval = "int|" +IntegerToString(WindowFirstVisibleBar());
    } else if (uCmd == "WindowHandle") {
        iPeriod=StrToInteger(uArg2);
        uRetval = "int|" +IntegerToString(WindowHandle(uArg1, iPeriod));
    } else if (uCmd == "WindowIsVisible") {
        iIndex=StrToInteger(uArg1);
        uRetval = "bool|" +WindowIsVisible(iIndex);
    } else if (uCmd == "WindowOnDropped") {
        uRetval = "int|" +IntegerToString(WindowOnDropped());
    } else if (uCmd == "WindowPriceMax") {
        iIndex=StrToInteger(uArg1);
        uRetval = "double|" +DoubleToStr(DoubleToStr(WindowPriceMax(iIndex), 2), 6);
    } else if (uCmd == "WindowPriceMin") {
        iIndex=StrToInteger(uArg1);
        uRetval = "double|" +DoubleToStr(DoubleToStr(WindowPriceMin(iIndex), 2), 6);
    } else if (uCmd == "WindowPriceOnDropped") {
        uRetval = "double|" +DoubleToStr(WindowPriceOnDropped(), 6);
    } else if (uCmd == "WindowRedraw") { //0
        WindowRedraw();
        uRetval = "void|";
        // WindowScreenShot
    } else if (uCmd == "WindowTimeOnDropped") {
        uRetval = "datetime|" +WindowTimeOnDropped();
    } else if (uCmd == "WindowXOnDropped") {
        uRetval = "int|" +IntegerToString(WindowXOnDropped());
    } else if (uCmd == "WindowYOnDropped") {
        uRetval = "int|" +IntegerToString(WindowYOnDropped());
    } else if (uCmd == "WindowsTotal") { //0
        uRetval = "int|" +IntegerToString(WindowsTotal());
    } else {
        uMsg="Unrecognized action: ";
        vWarn("zProcessCmdWin: " +uMsg +uCmd);
        uRetval = "";
    }

    return(uRetval);
}


string zProcessCmdAcc(string uCmd, string uChartId, string uIgnore, string uArg1, string uArg2, string uArg3, string uArg4, string uArg5) {
    string uMsg;
    string uRetval="";
    string uSymbol;
    int iCmd;
    double fVolume;

    if (uCmd == "AccountBalance") { //0
        uRetval = "double|" +DoubleToStr(AccountBalance(), 2);
    } else if (uCmd == "AccountCompany") { //0
        uRetval = "string|" +AccountCompany();
    } else if (uCmd == "AccountCredit") { //0
        uRetval = "double|" +DoubleToStr(AccountCredit(), 2);
    } else if (uCmd == "AccountCurrency") { //0
        uRetval = "string|" +AccountCurrency();
    } else if (uCmd == "AccountEquity") { //0
        uRetval = "double|" +DoubleToStr(AccountEquity(), 2);
    } else if (uCmd == "AccountFreeMargin") { //0
        uRetval = "double|" +DoubleToStr(AccountFreeMargin(), 2);
    } else if (uCmd == "AccountFreeMarginCheck") {
        // assert
        uSymbol=uArg1;
        iCmd=StrToInteger(uArg2);
        fVolume=StrToDouble(uArg3);
        uRetval = "double|" +DoubleToStr(AccountFreeMarginCheck(uSymbol, iCmd, fVolume), 2);
    } else if (uCmd == "AccountFreeMarginMode") { //0
        uRetval = "double|" +DoubleToStr(AccountFreeMarginMode(), 2);
    } else if (uCmd == "AccountLeverage") { //0
        uRetval = "int|" +IntegerToString(AccountLeverage());
    } else if (uCmd == "AccountMargin") { //0
        uRetval = "double|" +DoubleToStr(AccountMargin(), 2);
    } else if (uCmd == "AccountName") { //0
        uRetval = "string|" +AccountName();
    } else if (uCmd == "AccountNumber") { //0
        uRetval = "int|" +IntegerToString(AccountNumber());
    } else if (uCmd == "AccountProfit") { //0
        uRetval = "double|" +DoubleToStr(AccountProfit(), 2);
    } else if (uCmd == "AccountServer") { //0
        uRetval = "string|" +AccountServer();
    } else if (uCmd == "AccountStopoutLevel") { //0
        uRetval = "int|" +IntegerToString(AccountStopoutLevel());
    } else if (uCmd == "AccountStopoutMode") { //0
        uRetval = "int|" +IntegerToString(AccountStopoutMode());
    } else {
        uMsg="Unrecognized action: ";
        vWarn("zProcessCmdAcc: " +uMsg  +uCmd);
        uRetval="";
    }

    return(uRetval);
}

string zProcessCmdGlo(string uCmd, string uChartId, string uIgnore, string uArg1, string uArg2, string uArg3, string uArg4, string uArg5) {
    string uMsg;
    string uRetval="";
    string sName;
    double fValue;
    int iValue;

    if (uCmd == "GlobalVariableCheck") {
        // assert
        sName = uArg1;
        uRetval = "bool|" +GlobalVariableCheck(sName);
    } else if (uCmd == "GlobalVariableDel") {
        // assert
        sName = uArg1;
        uRetval = "bool|" +GlobalVariableDel(sName);
    } else if (uCmd == "GlobalVariableDeleteAll") {
        // assert
        sName = uArg1;
        iValue = StringToInteger(uArg2); //FixMe: datetime
        //FixMe uRetval = "bool|" +GlobalVariableDeleteAll(sName, iValue);
        uRetval = "bool|false";
    } else if (uCmd == "GlobalVariableGet") {
        // assert
        sName = uArg1;
        uRetval = "double|" +DoubleToStr(GlobalVariableGet(sName), 6);
        // overloaded
    } else if (uCmd == "GlobalVariableName") {
        // assert
        iValue = StringToInteger(uArg1);
        uRetval = "string|" +GlobalVariableName(iValue);
        // overloaded but we cant pass pointers
    } else if (uCmd == "GlobalVariableSet") {
        // assert
        sName = uArg1;
        fValue = StrToDouble(uArg2);
        uRetval = "double|" +DoubleToStr(GlobalVariableSet(sName, fValue), 6);
    } else {
        // GlobalVariableSetOnCondition
        uMsg = "Unrecognized action: ";
        vWarn("zProcessCmdGlo: " +uMsg +uCmd);
        uRetval = "";
    }

    return(uRetval);
}
