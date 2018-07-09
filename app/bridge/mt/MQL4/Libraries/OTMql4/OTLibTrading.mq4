// -*-mode: c; c-style: stroustrup; c-basic-offset: 4; coding: utf-8-dos -*-

#property copyright "Copyright 2013 OpenTrading"
#property link      "https://github.com/OpenTrading/"
#property library

// A More robust library of functions for Orders.

#include <stdlib.mqh>
#include <stderror.mqh>
#include <OTMql4/OTLibLog.mqh>
#include <OTMql4/OTLibConstants.mqh>
#include <OTMql4/OTLibServerErrors.mqh>

double fEPS=0.000001;

int iOTOrderSelect(int iIndex, int iSelect, int iPool=MODE_TRADES) {
    // returns 1 on success, 0 or -iError on failure
    bool bRetval;

    bRetval=OrderSelect(iIndex, iSelect, iPool);
    if (bRetval != true) {
        int iError=GetLastError();
        vWarn("Error selecting order # "+iIndex+
              ": "+ErrorDescription(iError) +"("+iError+")");
        return(-iError);
    }
    return(1);
}

int iOTOrderSendMarket(string uSymbol, int iCmd, double fVolume,
                       int iStops=5, int iProfits=10, int slippage=3) {
    //                  int slippage, double stoploss, double fTakeprofit,
    double fPrice, fBid, fAsk;
    double fStoploss;
    double fTakeprofit;
    double fMinstoplevel;
    int iRetval, iDigits;

    if (bOTIsTradeAllowed() == false) {
        // does iOTRefreshRates()
        return(-1);
    }
    fBid = MarketInfo(uSymbol, MODE_BID);
    //? assert >0
    fAsk = MarketInfo(uSymbol, MODE_ASK);
    //? assert >0
    fMinstoplevel = MarketInfo(uSymbol, MODE_STOPLEVEL);
    iDigits = (int) MarketInfo(uSymbol, MODE_DIGITS);

    if (iCmd == OP_BUY) {
        //--- calculated SL and TP fPrices must be normalized
        fStoploss = NormalizeDouble(fBid-iStops*fMinstoplevel*Point, iDigits);
        fTakeprofit = NormalizeDouble(fAsk+iProfits*fMinstoplevel*Point, iDigits);
        fPrice = NormalizeDouble(fAsk, iDigits);
    } else {
        //--- calculated SL and TP fPrices must be normalized
        fStoploss = NormalizeDouble(fBid-iStops*fMinstoplevel*Point, iDigits);
        fTakeprofit = NormalizeDouble(fAsk+iProfits*fMinstoplevel*Point, iDigits);
        fPrice = NormalizeDouble(fBid, iDigits);
    }

    iRetval = iOTOrderSend(uSymbol, iCmd,
                           fVolume, fPrice, slippage,
                           fStoploss, fTakeprofit);
    // 130 is invalid stops
    return(iRetval);
}

int iOTOrderSend(string uSymbol, int cmd,
                 double fVolume, double fPrice, int slippage,
                 double fStoploss, double fTakeprofit,
                 string comment="", int magic=0, datetime expiration=0,
                 color arrow_color=CLR_NONE) {
    // Returns number of the ticket assigned to the order by the trade server or -1 if it fails.
    int iRetval;
    bool bContinuable = true;
    int iError;
    int iTick = 0;

    iTick=0;
    iError=0;
    while (bContinuable == true && iTick < OT_MAX_TICK_RETRIES) {
        iTick += 1;

        if (iOTSetTradeIsBusy() != 1) {
            vWarn(" Unable to acquire the trade context. Retrying (try #" + iTick + ")");
            continue;
        }

        iRetval = OrderSend(uSymbol, cmd, fVolume, fPrice, slippage, fStoploss,
                            fTakeprofit, comment, magic, expiration, arrow_color);
        iOTSetTradeIsNotBusy();

        if (iRetval > 0) {return(iRetval);}

        iError=GetLastError();
        vWarn("Error sending order: " +ErrorDescription(iError) +"("+iError+")");
        // what about "no error"
        bContinuable = bOTLibServerErrorIsContinuable(iError);
        iRetval = -iError;
    }
    return(iRetval);
}

int iOTOrderCloseMarket(int iTicket, int iSlippage=3, color cColor=CLR_NONE) {
    // returns 1 on success, 0 or -iError on failure
    double fPrice=0.0;

    if (bOTIsTradeAllowed() == false) {
        // does iOTRefreshRates()
        return(-1);
    }
    //? use to default slippage?
    //fMinstoplevel = MarketInfo(uSymbol, MODE_STOPLEVEL);

    return(iOTOrderCloseFull(iTicket, fPrice, iSlippage, cColor));
}

int iOTOrderCloseFull(int iTicket, double fPrice, int iSlippage=3, color cColor=CLR_NONE) {
    // returns 1 on success, 0 or -iError on failure
    double fLots=0.0;
    return(iOTOrderClose(iTicket, fLots, fPrice, iSlippage, cColor));
}

int iOTOrderClose(int iTicket,  double fLots, double fPrice, int iSlippage, color cColor=CLR_NONE) {

    // returns 1 on success, 0 or -iError on failure
    bool bRetval;
    bool bContinuable = true;
    int iError, iCmd, iDigits;
    int iTick=0;
    string uSymbol;
    double fBid, fAsk;

    iTick=0;
    iError=0;
    while (bContinuable == true && iTick < OT_MAX_TICK_RETRIES) {
        iTick += 1;
        if (iOTSetTradeIsBusy() != 1) {
            vWarn(" Unable to acquire the trade context. Retrying (try #" +
                  iTick + ")");
            continue;
        }
        if (fLots < fEPS || fPrice < fEPS) {
            iError = iOTOrderSelect(iTicket, SELECT_BY_TICKET, MODE_TRADES);
            if (iError <= 0) {
                vWarn("Select order failed " +
                      " for order " + iTicket +
                      ": " + ErrorDescription(GetLastError()));
                // FixMe?: check the error for fatal ones
                continue;
            }
            if (fLots < fEPS) {
                fLots = OrderLots();
            }
            if (fPrice < fEPS) {
                uSymbol = OrderSymbol();
                iCmd = OrderType();
                iDigits = (int) MarketInfo(uSymbol, MODE_DIGITS);
                if (iCmd == OP_BUY) {
                    fBid = MarketInfo(uSymbol, MODE_BID);
                    //? assert >0
                    fPrice = NormalizeDouble(fBid, iDigits);
                } else {
                    fAsk = MarketInfo(uSymbol, MODE_ASK);
                    //? assert >0
                    fPrice = NormalizeDouble(fAsk, iDigits);
                }
            }
        }
        bRetval = OrderClose(iTicket, fLots, fPrice, iSlippage, cColor);
        iOTSetTradeIsNotBusy();
        if (bRetval == true) {
            return(1);
        }
        iError=GetLastError();
        vWarn("Error closing order # "+iTicket+
              ": "+ErrorDescription(iError) +"("+iError+")");

        // what about "no error"
        bContinuable = bOTLibServerErrorIsContinuable(iError);
    }

    return(-iError);
}

int iOTSetTradeIsBusy( int iMaxWaitingSeconds = 60 ) {
    /*
      from http://articles.mql4.com/141

      The function sets the global variable fTradeIsBusy value 0 with 1.
      If TradeIsBusy = 1 at the moment of launch, the function waits
      until TradeIsBusy is 0, and then replaces it with 1.0.
      If there is no global variable TradeIsBusy, the function creates it.

      Return codes:
      1 - successfully completed. The global variable TradeIsBusy was assigned 1
      -1 - TradeIsBusy = 1 at the moment of launch, the waiting was interrupted by the user
      (the expert was removed from the chart, the terminal was closed,
      the chart period and/or symbol was changed, etc.)
      -2 - TradeIsBusy = 1 at the moment of launch of the function, the
      waiting limit was exceeded (60 sec)
      -3 - No connection to server
    */
    int iError = 0;
    int StartWaitingTime;

    if(IsTesting()) return(1);
    if(!bOTIsTradeAllowed()) return(-3);
    //FixMe: something is broken below here and it may be overkill
    return(1);

    StartWaitingTime = GetTickCount();

    // Check whether a global variable exists and, if not, create it
    while(true) {
        // if the expert was terminated by the user, stop operation
        if(IsStopped()) {return(-1);}

        // if the waiting time exceeds that specified in the variable
        // iMaxWaitingSeconds, stop operation, as well
        if ((GetTickCount() - StartWaitingTime) > iMaxWaitingSeconds * 1000) {
            vWarn("Waiting time (" + iMaxWaitingSeconds + " sec.) exceeded!");
            return(-2);
        }
        // check whether the global variable exists
        // if it does, leave the loop and go to the block of changing
        // TradeIsBusy value
        if (GlobalVariableCheck( "fTradeIsBusy" )) break;

        // if the GlobalVariableCheck returns FALSE, it means that it does
        // not exist or an error has occurred during checking.
        iError = GetLastError();
        if (iError != 0) {
            vWarn("Error in TradeIsBusy GlobalVariableCheck(\"TradeIsBusy\"): " +
                  ErrorDescription(iError) );
            Sleep(OT_TRADE_ORDER_SLEEP_MSEC);
            continue;
        }

        // if there is no error, it means that there is just no global variable,
        // try to create it as a temporary global variable.
        // if the GlobalVariableSet > 0, it means that the global variable
        // has been successfully created. Leave the function.
        GlobalVariableTemp("fTradeIsBusy");
        if (GlobalVariableSet( "fTradeIsBusy", 1.0 ) > 0 ) {
            return(1);
        }
        // if the GlobalVariableSet has returned a value <= 0,
        // it means that an error occurred at creation of the variable
        iError = GetLastError();
        if(iError != 0) {
            vWarn("Error in TradeIsBusy GlobalVariableSet(\"TradeIsBusy\",0.0 ): " +
                  ErrorDescription(iError) );
            Sleep(OT_TRADE_ORDER_SLEEP_MSEC);
            continue;
        }
    }

    // If the function execution has reached this point, it means that
    // the global variable variable exists. Wait until the TradeIsBusy
    // becomes = 0 and change the value of TradeIsBusy to 1

    while(true) {
        // if the expert was terminated by the user, stop operation
        if(IsStopped()) return(-1);

        // if the waiting time exceeds that specified in the variable
        // iMaxWaitingSeconds, stop operation, as well
        if(GetTickCount() - StartWaitingTime > iMaxWaitingSeconds * 1000) {
            vWarn("Waiting time (" + iMaxWaitingSeconds + " sec.) exceeded!");
            return(-2);
        }
        // try to change the value of the TradeIsBusy from 0 to 1
        // if succeed, leave the function returning 1 ("successfully completed")
        if (GlobalVariableSetOnCondition( "fTradeIsBusy", 1.0, 0.0 )) {
            return(1);
        }
        // if not, 2 reasons for it are possible: TradeIsBusy = 1 (then one has to wait), or

        // an error occurred (this is what we will check)

        iError = GetLastError();
        // if it is still an error, display information and try again
        if(iError != 0) {
            vWarn("Error in TradeIsBusy GlobalVariableSetOnCondition(\"TradeIsBusy\",1.0,0.0 ):" +
                  ErrorDescription(iError) );
            continue;
        }

        // if there is no error, it means that TradeIsBusy = 1
        // (another expert is trading),
        // then display information and wait...
        vInfo("Waiting for the trade context to become free...");
        //? use refreshrates instead of sleep? - it can be slow
        // and may be called later on in the sequence that calls this
        Sleep(OT_TRADE_ORDER_SLEEP_MSEC);
    }
    /* should be unreached */
    return(0);

}


int iOTSetTradeIsNotBusy() {
    //  The function sets the value of the global variable fTradeIsBusy = 0.
    //  If the fTradeIsBusy does not exist, the function creates it.
    int iError;

    // if testing, just terminate
    if(IsTesting()) return(0);

    //FixMe: something is broken below here and it may be overkill
    return(0);

    while(true) {
        // if the expert was terminated by the user,
        if(IsStopped()) return(-1);

        // try to set the global variable value = 0
        // (or create the global variable)
        // if the GlobalVariableSet returns a value > 0, it means that everything
        // has succeeded. Leave the function
        if (GlobalVariableSet( "fTradeIsBusy", 0.0 ) > 0)
            return(1);

        // if the GlobalVariableSet returns a value <= 0,
        // this means that an error has occurred.
        // Display information, wait, and try again
        iError = GetLastError();
        if (iError != 0 ) {
            vWarn("Error in TradeIsNotBusy GlobalVariableSet(\"TradeIsBusy\",0.0): " +
                  ErrorDescription(iError) );
        }
        //? use refreshrates instead of sleep? - it can be slow
        // and may be called later on in the sequence that calls this
        Sleep(OT_TRADE_ORDER_SLEEP_MSEC);
    }
    /* should be unreached */
    return(0);
}


/*
fOTExposedEcuInMarket shows how much worse thing could get, unlike
AccountMargin which shows how bad things are now.  It's the worst case sum
of Open against the order's fStoploss * return value < 0 means we have
exposure * iOrderEAMagic=0 gives us exposed margin for ALL orders, ours or not.
*/

double fOTExposedEcuInMarket(int iOrderEAMagic = 0) {
    string uSymbol;
    int i;
    int iRetval;
    double fStopLoss;
    double fExposedEcu=0.0;

    for(i=OrdersTotal()-1; i>=0; i--) {

        iRetval = iOTOrderSelect(i, SELECT_BY_POS, MODE_TRADES);
        if (iRetval <= 0) {
            vWarn("Select order failed " +
                  " for order " + i +
                  ": " + ErrorDescription(GetLastError()));
            continue;
        }

        if (iOrderEAMagic > 0 && OrderMagicNumber() != iOrderEAMagic) continue;

        fStopLoss = OrderStopLoss();
        if (fStopLoss < fEPS) {
            vWarn("The exposure is probably infinite " +
                  " for order " + OrderTicket() +" (no stoploss)");
            fExposedEcu = AccountFreeMargin();
            return(fExposedEcu);
        }

        int iType = OrderType(); // Order type
        double fOrderLots = OrderLots();
        uSymbol = OrderSymbol();
        // FixMe: check retval
        double fLotSize = MarketInfo(uSymbol, MODE_LOTSIZE);
        double fOpenPrice = OrderOpenPrice();
        double fMarginRequired = MarketInfo(uSymbol, MODE_MARGINREQUIRED);

        double fWorstCase;
        if (iType == OP_BUY) {
            if (fStopLoss < Bid) {
                fWorstCase = (Bid-fStopLoss)/Bid*fMarginRequired;
                fExposedEcu += fWorstCase * fOrderLots * fLotSize;
                vDebug("Exposure on order # "+i+
                       " fExposure="+ (fWorstCase * fOrderLots * fLotSize )+
                       " Bid="+Bid+
                       " fStopLoss="+fStopLoss+
                       " lots fMarginRequired="+fMarginRequired*fOrderLots * fLotSize);
            }
        } else if (iType == OP_SELL) {
            if (fStopLoss > Ask) {
                fWorstCase = (fStopLoss-Ask)/Ask*fMarginRequired;
                fExposedEcu += fWorstCase * fOrderLots * fLotSize;
                vDebug("Exposure on order # "+i+
                       " fExposure="+ (fWorstCase * fOrderLots * fLotSize)+
                       " Ask="+Ask+
                       " fStopLoss="+fStopLoss+
                       " lots fMarginRequired="+fMarginRequired*fOrderLots * fLotSize);
            }
        }
    }

    return(fExposedEcu);
}

bool bOTIsTradeAllowed() {
    /*
      Wait for the trade context to become free.
      Returns true if the trade context is free.

      You probably want to use this in place of RefreshRates:
      it checks IsTradeAllowed and runs RefreshRates.

      Warning: RefreshRates can take a long time.
    */
    int iTicks = 0;

    if (IsTesting() || IsOptimization()) return (true);
    if (IsConnected() == false) {
        vWarn("Unable to trade : not connected");
        return(false);
    }

    while( IsTradeAllowed() == false && iTicks < OT_MAX_TICK_RETRIES) {
        iTicks += 1;
         // use refresh rates to Cycle delay
        if (iOTRefreshRates() < 0) {
            return(false);
        }
    }
    if (iTicks >= OT_MAX_TICK_RETRIES) {
        vWarn("Unable to get TradeAllowed context for : "+
              " in " + OT_MAX_TICK_RETRIES + " tries.");
        return(false);
    }
    return (true);
}

int iOTRefreshRates() {
    /*
      Returns 0 on success or -iError on failure

      Warning: RefreshRates can take a long time.
    */
    int iTicks=0;

    if (IsTesting() || IsOptimization()) return (0);
    if (IsConnected() == false) {
        vWarn("Unable to refresh rates : not connected");
        return(-1);
    }

    while(RefreshRates() == false && iTicks < OT_MAX_TICK_RETRIES) {
        iTicks += 1;
        Sleep(OT_TICK_SLEEP_MSEC); // Cycle delay
    }

    if (iTicks >= OT_MAX_TICK_RETRIES) {
        vWarn("Unable to refresh rates"+
              " in " +OT_TICK_SLEEP_MSEC +"tries.");
        return(-2);
    }
    return(0);
 }
/* This is wrong: MarketInfo returns many types */
int iOTMarketInfo(string s, int iMode) {
    /*
      Before using the MarketInfo() you should use the function  RefreshRates()
      to be sure that we getting the up-to-date market data.

    */
    int iRetval;
    int iError;
    if (s == "") {
        vWarn("iOTMarketInfo - Empty symbol for getting "+iMode);
        return(-1);
    }
    if (iMode <= 0) {
        vWarn("iOTMarketInfo - Negative mode for getting "+iMode+" for "+s);
        return(-1);
    }
    iRetval = MarketInfo(s, iMode);
    iError = GetLastError();
    if (iError > 0) {
        vWarn("Error getting " +iMode +" for " +s
              +": "+ErrorDescription(iError));
        return(-iError);
    }
    return(iRetval);
}

double fOTMarketInfo(string s, int iMode) {
    /*
      Before using the MarketInfo() you should use the function  RefreshRates()
      to be sure that we getting the up-to-date market data.

    */
    int iError;
    double fRetval;

    if (s == "") {
        vWarn("iOTMarketInfo - Empty symbol for getting "+iMode);
        return(-1.0);
    }
    if (iMode <= 0) {
        vWarn("iOTMarketInfo - Negative mode for getting "+iMode+" for "+s);
        return(-2.0);
    }
    fRetval = MarketInfo(s, iMode);
    iError = GetLastError();
    if (iError > 0) {
        vWarn("Error getting " +iMode +" for " +s
              +": "+ErrorDescription(iError));
        return(-iError*1.0);
    }
    return(fRetval);
}

// FixMe: should be per iTicket with uSymbol derived
bool bOTModifyTrailingStopLoss(string uSymbol, int iTrailingStopLossPoints,
                               datetime tExpiration=0) {
    // return value of false signals an error

    string sMsg;
    bool bRetval=true;
    int iRetval, i, iDigits;
    int iType, iMinDistance;
    double fTakeProfit;
    double fPrice;
    int iTicket;
    double fStopLoss;
    double fTrailingStopLoss;
    bool bModify;


    for(i=OrdersTotal()-1; i>=0; i--) {
        iRetval = OrderSelect(i, SELECT_BY_POS, MODE_TRADES);
        if (iRetval < 0) {bRetval=false; continue;}

        // Analysis of orders:
        iType = OrderType(); // Order type
        if (OrderSymbol() != uSymbol || iType > 1) continue;
        iMinDistance = MarketInfo(uSymbol, MODE_STOPLEVEL);
        if (iMinDistance < 0) {bRetval=false; continue;}

        fTakeProfit = OrderTakeProfit(); // TakeProfit of the selected order
        fPrice = OrderOpenPrice(); // Price of the selected order
        iTicket = OrderTicket(); // Ticket of the selected order
        fStopLoss = OrderStopLoss(); // SL of the selected order
        iDigits = (int) MarketInfo(uSymbol, MODE_DIGITS);

        fTrailingStopLoss = iTrailingStopLossPoints; // Initial value
        if (fTrailingStopLoss < iMinDistance) {
            // If less than allowed
            fTrailingStopLoss = iMinDistance;
        }

        bModify = false; // Not to be modified
        switch(iType) {
        case OP_BUY: // Order Buy 0
            if (NormalizeDouble(fStopLoss, iDigits) < // If it is lower than we want
                NormalizeDouble(Bid-fTrailingStopLoss*Point, iDigits) &&
                Bid-fTrailingStopLoss*Point > fTrailingStopLoss*Point/10.0 //? why
                ) {
                fStopLoss = Bid-fTrailingStopLoss*Point; // then modify it
                sMsg = "Buy ";
                bModify = true; // To be modified
            }
            break; // Exit 'switch'
        case OP_SELL: // Order Sell 1
            if (NormalizeDouble(fStopLoss, iDigits) > // If it is higher than we want
                NormalizeDouble(Ask+fTrailingStopLoss*Point, iDigits) &&
                Ask+fTrailingStopLoss*Point > fTrailingStopLoss*Point/10.0 //? why
                ) {
                // || NormalizeDouble(fStopLoss, Digits)==0 //or equal to zero
                fStopLoss=Ask+fTrailingStopLoss*Point; // then modify it
                sMsg = "Sell ";
                bModify = true;
            }
        }

        if (bModify==false) continue;

        bRetval = bRetval && bOTModifyOrder("Modifiying stoploss "+sMsg,
                                            iTicket, fPrice,
                                            fStopLoss, fTakeProfit,
                                            tExpiration);
    }

    return(bRetval);
}

bool bOTModifyOrder(string sMsg,
                  int iTicket,
                  double fPrice,
                  double fStopLoss,
                  double fTakeProfit,
                  datetime tExpiration) {
    // FixMe: how do we check and order has been selected?
    int iRetry=0;
    int iTicks, iDigits;
    bool bAns;
    bool bRetval=false;
    string uSymbol;

    uSymbol = OrderSymbol();
    iDigits = (int) MarketInfo(uSymbol, MODE_DIGITS);
    while(iRetry < OT_MAX_TICK_RETRIES) {
        // Modification cycle
        iRetry += 1;
        vInfo(sMsg +iTicket +" at " +Bid
              +" from sl " +OrderStopLoss()+" to " +fStopLoss
              +" from tp " +OrderTakeProfit()+" to " +fTakeProfit
              +". Awaiting response.");
        bAns = OrderModify(iTicket, NormalizeDouble(fPrice, iDigits),
                         NormalizeDouble(fStopLoss, iDigits),
                         NormalizeDouble(fTakeProfit, iDigits),
                         tExpiration);

        if (IsTesting() || IsOptimization() || bAns==true) {
            vInfo("Order " +sMsg+iTicket +" is modified: ");
            return(true);
        }

        if (bOTContinueOnOrderError(iTicket)) {
            iTicks = 0;
            while ( RefreshRates()==false && iTicks < OT_MAX_TICK_RETRIES) {
                // To the new tick
                iTicks +=  1;
                Sleep(OT_TICK_SLEEP_MSEC); // Cycle delay
            }
            if (iTicks >= OT_MAX_TICK_RETRIES) {break;}
        }
    }

    vWarn("Error modifying Order # " +iTicket +": "
          // +" " +ErrorDescription(iError)
          );
    return(bRetval);
}

bool bOTContinueOnOrderError(int iTicket) {
    bool bContinue=false;
    int iError=GetLastError();

    switch(iError) {
        // Overcomable errors
    case 130:
        Print("Wrong stops. Retrying.");
        bContinue=true; break; // At the next iteration
    case 136:
        Print("No prices. Waiting for a new tick..");
        bContinue=true; break; // At the next iteration
    case 146:
        Print("Trading subsystem is busy. Retrying ");
        bContinue=true; break; // At the next iteration
        // Critical errors
    case 1 :
        Print("No error."); // WTF?
        break; // Exit 'switch'
    default:
        bContinue=bOTLibServerErrorIsContinuable(iError);
        break;
    }
    return(bContinue);
}

