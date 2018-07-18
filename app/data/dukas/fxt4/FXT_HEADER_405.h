/**
 * MT4 structure FXT_HEADER version 405 (tick file header).
 */
struct FXT_HEADER {                                // -- offset ---- size --- description ----------------------------------------------------------------------------
   UINT   version;                                 //         0         4     header version:                             405
   char   description[64];                         //         4        64     copyright/description (szchar)
   char   serverName[128];                         //        68       128     account server name (szchar)
   char   symbol[MAX_SYMBOL_LENGTH+1];             //       196        12     symbol (szchar)
   UINT   period;                                  //       208         4     timeframe in minutes
   UINT   modelType;                               //       212         4     0=EveryTick|1=ControlPoints|2=BarOpen
   UINT   modeledBars;                             //       216         4     number of modeled bars      (w/o prolog)
   UINT   firstBarTime;                            //       220         4     bar open time of first tick (w/o prolog)
   UINT   lastBarTime;                             //       224         4     bar open time of last tick  (w/o prolog)
   BYTE   reserved_1[4];                           //       228         4     (alignment to the next double)
   double modelQuality;                            //       232         8     max. 99.9

   // common parameters                            // ----------------------------------------------------------------------------------------------------------------
   char   baseCurrency[MAX_SYMBOL_LENGTH+1];       //       240        12     base currency (szchar)                     = StringLeft(symbol, 3)
   UINT   spread;                                  //       252         4     spread in points: 0=zero spread            = MarketInfo(MODE_SPREAD)
   UINT   digits;                                  //       256         4     digits                                     = MarketInfo(MODE_DIGITS)
   BYTE   reserved_2[4];                           //       260         4     (alignment to the next double)
   double pointSize;                               //       264         8     resolution, ie. 0.0000'1                   = MarketInfo(MODE_POINT)
   UINT   minLotsize;                              //       272         4     min lot size in centi lots (hundredths)    = MarketInfo(MODE_MINLOT)  * 100
   UINT   maxLotsize;                              //       276         4     max lot size in centi lots (hundredths)    = MarketInfo(MODE_MAXLOT)  * 100
   UINT   lotStepsize;                             //       280         4     lot stepsize in centi lots (hundredths)    = MarketInfo(MODE_LOTSTEP) * 100
   UINT   stopsLevel;                              //       284         4     orders stop distance in points             = MarketInfo(MODE_STOPLEVEL)
   BOOL   pendingsGTC;                             //       288         4     close pending orders at end of day or GTC
   BYTE   reserved_3[4];                           //       292         4     (alignment to the next double)

   // profit calculation parameters                // ----------------------------------------------------------------------------------------------------------------
   double contractSize;                            //       296         8     ie. 100000                                 = MarketInfo(MODE_LOTSIZE)
   double tickValue;                               //       304         8     tick value in quote currency (empty)       = MarketInfo(MODE_TICKVALUE)
   double tickSize;                                //       312         8     tick size (empty)                          = MarketInfo(MODE_TICKSIZE)
   UINT   profitCalculationMode;                   //       320         4     0=Forex|1=CFD|2=Futures                    = MarketInfo(MODE_PROFITCALCMODE)

   // swap calculation parameters                  // ----------------------------------------------------------------------------------------------------------------
   BOOL   swapEnabled;                             //       324         4     if swaps are to be applied
   UINT   swapCalculationMode;                     //       328         4     0=Points|1=BaseCurrency|2=Interest|3=MarginCurrency   = MarketInfo(MODE_SWAPTYPE)
   BYTE   reserved_4[4];                           //       332         4     (alignment to the next double)
   double swapLongValue;                           //       336         8     long overnight swap value                  = MarketInfo(MODE_SWAPLONG)
   double swapShortValue;                          //       344         8     short overnight swap values                = MarketInfo(MODE_SWAPSHORT)
   UINT   tripleRolloverDay;                       //       352         4     weekday of triple swaps                    = WEDNESDAY (3)

   // margin calculation parameters                // ----------------------------------------------------------------------------------------------------------------
   UINT   accountLeverage;                         //       356         4     account leverage                           = AccountLeverage()
   UINT   freeMarginCalculationType;               //       360         4     free margin calculation type               = AccountFreeMarginMode()
   UINT   marginCalculationMode;                   //       364         4     margin calculation mode                    = MarketInfo(MODE_MARGINCALCMODE)
   UINT   marginStopoutLevel;                      //       368         4     margin stopout level                       = AccountStopoutLevel()
   UINT   marginStopoutType;                       //       372         4     margin stopout type                        = AccountStopoutMode()
   double marginInit;                              //       376         8     initial margin requirement (in units)      = MarketInfo(MODE_MARGININIT)
   double marginMaintenance;                       //       384         8     maintainance margin requirement (in units) = MarketInfo(MODE_MARGINMAINTENANCE)
   double marginHedged;                            //       392         8     hedged margin requirement (in units)       = MarketInfo(MODE_MARGINHEDGED)
   double marginDivider;                           //       400         8     leverage calculation                         @see example in struct SYMBOL
   char   marginCurrency[MAX_SYMBOL_LENGTH+1];     //       408        12                                                = AccountCurrency()
   BYTE   reserved_5[4];                           //       420         4     (alignment to the next double)

   // commission calculation parameters            // ----------------------------------------------------------------------------------------------------------------
   double commissionValue;                         //       424         8     commission rate
   UINT   commissionCalculationMode;               //       432         4     0=Money|1=Pips|2=Percent                     @see COMMISSION_MODE_*
   UINT   commissionType;                          //       436         4     0=RoundTurn|1=PerDeal                        @see COMMISSION_TYPE_*

   // later additions                              // ----------------------------------------------------------------------------------------------------------------
   UINT   firstBar;                                //       440         4     bar number/index??? of first bar (w/o prolog) or 0 for first bar
   UINT   lastBar;                                 //       444         4     bar number/index??? of last bar (w/o prolog) or 0 for last bar
   UINT   startPeriodM1;                           //       448         4     bar index where modeling started using M1 bars
   UINT   startPeriodM5;                           //       452         4     bar index where modeling started using M5 bars
   UINT   startPeriodM15;                          //       456         4     bar index where modeling started using M15 bars
   UINT   startPeriodM30;                          //       460         4     bar index where modeling started using M30 bars
   UINT   startPeriodH1;                           //       464         4     bar index where modeling started using H1 bars
   UINT   startPeriodH4;                           //       468         4     bar index where modeling started using H4 bars
   UINT   testerSettingFrom;                       //       472         4     begin date from tester settings
   UINT   testerSettingTo;                         //       476         4     end date from tester settings
   UINT   freezeDistance;                          //       480         4     order freeze level in points               = MarketInfo(MODE_FREEZELEVEL)
   UINT   modelErrors;                             //       484         4     number of errors during model generation (FIX ERRORS SHOWING UP HERE BEFORE TESTING)
   BYTE   reserved_6[240];                         //       488       240     unused
};                                                 // ----------------------------------------------------------------------------------------------------------------
                                                   //               = 728
