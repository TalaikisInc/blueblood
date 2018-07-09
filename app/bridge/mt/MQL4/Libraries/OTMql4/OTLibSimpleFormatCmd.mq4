// -*-mode: c; c-style: stroustrup; c-basic-offset: 4; coding: utf-8-dos -*-

#property copyright "Copyright 2013 OpenTrading"
#property link      "https://github.com/OpenTrading/"
#property library

//  This is the replacement for what should be Eval in Mt4:
//  it takes a string expression and evaluates it.
//
//  I know this is verbose and could be done more compactly,
//  but it's clean and robust so I'll leave it like this for now.
//
//  If you want to extend this for your own functions you have declared in Mql4,
//  look at how OTLibProcessCmd.mq4 calls zMt4LibProcessCmd and then
//  goes on and handles it if zMt4LibProcessCmd didn't.
//

#include <stdlib.mqh>
#include <stderror.mqh>
#include <OTMql4/OTLibLog.mqh>
#include <OTMql4/OTLibStrings.mqh>
#include <OTMql4/OTLibSimpleFormatCmd.mqh>

string zOTLibSimpleFormatCmd(string uType, string uChartId, int iIgnore, string uMark, string uCmd) {
    //  uType is cmd or exec
    //  Both will be handled by ProcessCmd, but
    //  cmd commands will be put back on the wire as a retval.
    //  If  uType is not cmd or exec then "" is returned to signal failure.
    //
    string uRetval;
    if (uType != "cmd" && uType != "exec") {
        return("");
    }
    // FixMe: uBAR
    uRetval = StringFormat("%s|%s|%d|%s|%s", uType, uChartId, iIgnore, uMark, uCmd);
    return(uRetval);
}

string zOTLibSimpleFormatBar(string uType, string uChartId, int iIgnore, string uMark, string uInfo) {
    //  uType should be one of: bar
    //  Both will be put on the wire as a their type topics.
    //  If uType is not tick timer or bar, then "" is returned to signal failure.

    string uRetval;
    if (uType != "bar") {
        return("");
    }
    // FixMe: uBAR
    uRetval = StringFormat("%s|%s|%d|%s|%s", uType, uChartId, iIgnore, uMark, uInfo);
    return(uRetval);
}

string zOTLibSimpleFormatTimer(string uType, string uChartId, int iIgnore, string uMark, string uInfo) {
    //  uType should be one of: tick or timer
    //  Both will be put on the wire as a their type topics.
    //  If uType is not tick timer or bar, then "" is returned to signal failure.
    //
    string uRetval;
    if (uType != "timer") {
        return("");
    }
    // FixMe: uBAR
    uRetval = StringFormat("%s|%s|%d|%s|%s", uType, uChartId, iIgnore, uMark, uInfo);
    return(uRetval);
}

string zOTLibSimpleFormatTick(string uType, string uChartId, int iIgnore, string uMark, string uInfo) {
    //  uType should be one of: tick or timer
    //  Both will be put on the wire as a their type topics.
    //  If  uType is not tick timer or bar, then "" is returned to signal failure.
    //
    string uRetval;
    if (uType != "tick") {
        return("");
    }
    // FixMe: uBAR
    uRetval = StringFormat("%s|%s|%d|%s|%s", uType, uChartId, iIgnore, uMark, uInfo);
    return(uRetval);
}

string zOTLibSimpleFormatRetval(string uType, string uChartId, int iIgnore, string uMark, string uInfo) {
    //  uType should be one of: retval
    //  Will be put on the wire as a its type topic.
    //  If  uType is not retval, then "" is returned to signal failure.
    //
    string uRetval;
    if (uType != "retval") {
        return("");
    }
    if (uMark == "") {
        // Its already included in uInfo
        uRetval = StringFormat("%s|%s|%d|%s", uType, uChartId, iIgnore, uInfo);
    } else {
    // FixMe: uBAR
        uRetval = StringFormat("%s|%s|%d|%s|%s", uType, uChartId, iIgnore, uMark, uInfo);
    }
    return(uRetval);
}

string eOTLibSimpleUnformatCmd(string& aArrayAsList[]) {
    /*
     */
    string uType, uChartId, uIgnore, uMark, uCmd;
    string uArg1="";
    string uArg2="";
    string uArg3="";
    string uArg4="";
    string uArg5="";
    string uArg6="";
    string uArg7="";
    int iLen;
    string eRetval;

    iLen = ArraySize(aArrayAsList);
    if (iLen < 1) {
        eRetval = "eOTLibSimpleUnformatCmd iLen=0: split failed with " +uBAR;
        return(eRetval);
    }
    uType = StringTrimRight(aArrayAsList[0]);

    if (iLen < 2) {
        eRetval = "eOTLibSimpleUnformatCmd: split failed on field 2 ";
        return(eRetval);
    }
    uChartId = StringTrimRight(aArrayAsList[1]);

    if (iLen < 3) {
        eRetval = "eOTLibSimpleUnformatCmd: split failed on field 3 ";
        return(eRetval);
    }
    uIgnore = StringTrimRight(aArrayAsList[2]);

    if (iLen < 4) {
        eRetval = "eOTLibSimpleUnformatCmd: split failed on field 4 ";
        return(eRetval);
    }
    uMark = StringTrimRight(aArrayAsList[3]);
    if (StringLen(uMark) < 6) {
        eRetval = "eOTLibSimpleUnformatCmd uMark: too short " +uMark;
        return(eRetval);
    }
    if (iLen <= 4) {
        eRetval = "eOTLibSimpleUnformatCmd: split failed on field 5 ";
        return(eRetval);
    }
    uCmd = StringTrimRight(aArrayAsList[4]);

    if (iLen > 5) {
        uArg1 = StringTrimRight(aArrayAsList[5]);
        if (iLen > 6) {
            uArg2 = StringTrimRight(aArrayAsList[6]);
            if (iLen > 7) {
                uArg3 = StringTrimRight(aArrayAsList[7]);
                if (iLen > 8) {
                    uArg4 = StringTrimRight(aArrayAsList[8]);
                    if (iLen > 9) {
                        uArg5 = StringTrimRight(aArrayAsList[9]);
                        if (iLen > 10) {
                            uArg6 = StringTrimRight(aArrayAsList[10]);
                            if (iLen > 11) {
                                uArg7 = StringTrimRight(aArrayAsList[11]);
                            }
                        }
                    }
                }
            }
        }
    }
    ArrayResize(aArrayAsList, 12);
    aArrayAsList[0] = uType;
    aArrayAsList[1] = uChartId;
    aArrayAsList[2] = uIgnore;
    aArrayAsList[3] = uMark;
    aArrayAsList[4] = uCmd;
    aArrayAsList[5] = uArg1;
    aArrayAsList[6] = uArg2;
    aArrayAsList[7] = uArg3;
    aArrayAsList[8] = uArg4;
    aArrayAsList[9] = uArg5;
    aArrayAsList[10] = uArg6;
    aArrayAsList[11] = uArg7;
    return("");
}

