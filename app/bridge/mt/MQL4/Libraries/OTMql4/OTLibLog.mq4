// -*-mode: c; c-style: stroustrup; c-basic-offset: 4; coding: utf-8-dos -*-

//  This will provide our logging functions, but is just a
//  skeleton for now. See OTLibPyLog for logging with Python.

#property copyright "Copyright 2014 Open Trading"
#property link      "https://github.com/OpenTrading/"
#property library

// constants
#define OT_LOG_PANIC 0 // unused
#define OT_LOG_ERROR 1
#define OT_LOG_WARN 2
#define OT_LOG_INFO 3
#define OT_LOG_DEBUG 4
#define OT_LOG_TRACE 5

int iDefaultLoglevel = OT_LOG_DEBUG;

/* floating point rounding error */
double fEPSILON=0.01;

void vLogInit() {
    //  Initializes the logging environment. This should be called
    //  from your OnInit() function. It is safe to call it a second time;
    //  subsequent calls will just be ignored.

    /* not Tmp */
    if (GlobalVariableCheck("fDebugLevel") == false) {
        /* 1= Error, 2 = Warn, 3 = Info, 4 = Debug, 5 = Trace */
        GlobalVariableSet("fDebugLevel", iDefaultLoglevel);
    }
}

void vSetLogLevel(int i) {
    GlobalVariableSet("fDebugLevel", i);
}

int iGetLogLevel() {
    int iDebugLevel;
    double fDebugLevel;

    fDebugLevel = GlobalVariableGet("fDebugLevel");
    if (fDebugLevel < fEPSILON) {
    iDebugLevel = iDefaultLoglevel;
    GlobalVariableSet("fDebugLevel", iDebugLevel);
    } else {
    iDebugLevel = MathRound(fDebugLevel);
    }
    return(iDebugLevel);
}

void vLog(int iLevel, string sMess) {
    if (iLevel <= iGetLogLevel() ) {
        Print(sMess);
    }
}

void vError(string sMess) {
    vLog(OT_LOG_ERROR, "ERROR: "+sMess);
}

void vWarn(string sMess) {
    vLog(OT_LOG_WARN, "WARN: "+sMess);
}

void vInfo(string sMess) {
    vLog(OT_LOG_INFO, "INFO: "+sMess);
}

void vDebug(string sMess) {
    vLog(OT_LOG_DEBUG, "DEBUG: "+sMess);
}

void vTrace(string sMess) {
    vLog(OT_LOG_TRACE, "TRACE: "+sMess);
}
