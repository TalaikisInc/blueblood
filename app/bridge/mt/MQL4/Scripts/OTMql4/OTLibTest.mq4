// -*-mode: c; c-style: stroustrup; c-basic-offset: 4; coding: utf-8-dos -*-

#property copyright "Copyright 2014 Open Trading"
#property link      "https://github.com/OpenTrading/"

//  A simple test Script that doesn't do much, but it's a start.
//  Attach it to a chart, select the tests you want to run,
//  and a MessageBox will pop up to tell you if it passed or failed.

#property show_inputs

#include <OTMql4/OTLibLog.mqh>
#include <OTMql4/OTLibStrings.mqh>
#include <OTMql4/OTLibProcessCmd.mqh>

#include <WinUser32.mqh>

//  We will put each test as a boolean external input so the user
//  can select which tests to run.

extern bool bTestStrings=true;
extern bool bTestOTLibProcessCmd=true;

double fEps=0.000001;

void vAlert(string uText) {
    MessageBox(uText, "OTLibTest.mq4", MB_OK|MB_ICONEXCLAMATION);
}

string eTestStrings() {
    //  Test our parsing of strings with vStringToArray
    //
    int iErr = 0;
    string uRetval = "";
    string uArg;
    string aOutput[];

    uArg = "one";
    vStringToArray(uArg, aOutput, "|");
    if (ArraySize(aOutput) == 1) {
        Print("INFO: ArraySize(aOutput) == 1 -> " +uArg);
    } else {
        return("ERROR: ArraySize(aOutput) != 1 -> " +uArg);
    }

    uArg = "one|two|three";
    vStringToArray(uArg, aOutput, "|");
    if (ArraySize(aOutput) == 3) {
        Print("INFO: ArraySize(aOutput) == 3 -> " +uArg);
    } else {
        return("ERROR: ArraySize(aOutput) != 3 -> " +uArg);
    }
    return("");
}

string eTestOTLibProcessCmd() {
    int iErr = 0;
    string uRetval = "";
    string uArg;
    string aOutput[];
    string uExpect;

    uArg = "one";
    uRetval = zOTLibProcessCmd(uArg);
    if (StringCompare(uRetval, "") == 0) {
        Print("INFO: GOOD there be an error message in the Experts Log -> " +uArg);
    } else {
        return("ERROR: should NOT have returned a value -> " +uRetval);
    }

    uArg = "exec|USDUSD|0|123456|TerminalPath";
    uRetval = zOTLibProcessCmd(uArg);
    uExpect = "123456|string|" +TerminalPath();
    if (uRetval == uExpect) {
        Print("INFO: GOOD right answer -> " +uArg);
    } else {
        return("ERROR: wrong return value -> " +uRetval);
    }
    return("");
}

void OnStart() {
    string uRetval = "";
    int i = 0;
    if ( bTestStrings == true ) {
        uRetval = eTestStrings();
        if (uRetval != "") {
            vAlert(uRetval);
        } else {
            i = i + 1;
        }
    }
    if ( bTestOTLibProcessCmd == true ) {
        uRetval = eTestOTLibProcessCmd();
        if (uRetval != "") {
            vAlert(uRetval);
        } else {
            i = i + 1;
        }
    }
    if ( i > 0 ) {
        uRetval = "INFO: tests completed";
        vAlert(uRetval);
    }
}

void OnDeinit(const int iReason) {
}
