//+------------------------------------------------------------------+
//|                                                    FXTHeader.mqh |
//|                 Copyright © 2006-2007, MetaQuotes Software Corp. |
//|                                        http://www.metaquotes.net |
//+------------------------------------------------------------------+

#define FXT_VERSION         405

//---- profit calculation mode
#define PROFIT_CALC_FOREX     0
#define PROFIT_CALC_CFD       1
#define PROFIT_CALC_FUTURES   2
//---- type of swap
#define SWAP_BY_POINTS        0
#define SWAP_BY_DOLLARS       1
#define SWAP_BY_INTEREST      2
//---- free margin calculation mode
#define MARGIN_DONT_USE       0
#define MARGIN_USE_ALL        1
#define MARGIN_USE_PROFIT     2
#define MARGIN_USE_LOSS       3
//---- margin calculation mode
#define MARGIN_CALC_FOREX     0
#define MARGIN_CALC_CFD       1
#define MARGIN_CALC_FUTURES   2
#define MARGIN_CALC_CFDINDEX  3
//---- stop out check mode
#define MARGIN_TYPE_PERCENT   0
#define MARGIN_TYPE_CURRENCY  1
//---- basic commission type
#define COMM_TYPE_MONEY       0
#define COMM_TYPE_PIPS        1
#define COMM_TYPE_PERCENT     2
//---- commission per lot or per deal
#define COMMISSION_PER_LOT    0
#define COMMISSION_PER_DEAL   1

//---- FXT file header
int      i_version=FXT_VERSION;                                                        //    0 = 0x0000 + 4
string   s_copyright="(C)opyright 2005-2007, MetaQuotes Software Corp."; // 64 bytes   //    4 = 0x0004 + 64
string   s_server;                                   // 128 bytes                      //   68 = 0x0044 + 128
string   s_symbol;                                   // 12 bytes                       //  196 = 0x00C4 + 12
int      i_period;                                                                     //  208 = 0x00D0 + 4
int      i_model=0;                                  // every tick model               //  212 = 0x00D4 + 4
int      i_bars=0;                                   // bars processed                 //  216 = 0x00D8 + 4
datetime t_fromdate=0;                               // begin modelling date           //  220 = 0x00DC + 4
datetime t_todate=0;                                 // end modelling date             //  224 = 0x00E0 + 4
//++++ add 4 bytes to align the next double                                            +++++++
double   d_modelquality=99.0;                                                          //  232 = 0x00E4 + 8
//---- common parameters                                                               -------
string   s_currency;                                 // base currency (12 bytes)       //  240 = 0x00F0 + 12
int      i_spread;                                                                     //  252 = 0x00FC + 4
int      i_digits;                                                                     //  256 = 0x0100 + 4
//++++ add 4 bytes to align the next double                                            +++++++
double   d_point;                                                                      //  264 = 0x0108 + 8
int      i_lot_min;                                  // minimal lot size               //  272 = 0x0110 + 4
int      i_lot_max;                                  // maximal lot size               //  276 = 0x0114 + 4
int      i_lot_step;                                                                   //  280 = 0x0118 + 4
int      i_stops_level;                              // stops level value              //  284 = 0x011C + 4
bool     b_gtc_pendings=false;                       // good till cancel               //  288 = 0x0120 + 4
//---- profit calculation parameters                                                   -------
//++++ add 4 bytes to align the next double                                            +++++++
double   d_contract_size;                                                              //  296 = 0x0128 + 8
double   d_tick_value;                                                                 //  304 = 0x0130 + 8
double   d_tick_size;                                                                  //  312 = 0x0138 + 8
int      i_profit_mode=PROFIT_CALC_FOREX;            // profit calculation mode        //  320 = 0x0140 + 4
//---- swaps calculation                                                               -------
bool     b_swap_enable=true;                                                           //  324 = 0x0144 + 4
int      i_swap_type=SWAP_BY_POINTS;                 // type of swap                   //  328 = 0x0148 + 4
//++++ add 4 bytes to align the next double                                            +++++++
double   d_swap_long;                                                                  //  336 = 0x0150 + 8
double   d_swap_short;                               // overnight swaps values         //  344 = 0x0158 + 8
int      i_swap_rollover3days=3;                     // number of day of triple swaps  //  352 = 0x0160 + 4
//---- margin calculation                                                              -------
int      i_leverage=100;                                                               //  356 = 0x0164 + 4
int      i_free_margin_mode=MARGIN_USE_ALL;          // free margin calculation mode   //  360 = 0x0168 + 4
int      i_margin_mode=MARGIN_CALC_FOREX;            // margin calculation mode        //  364 = 0x016C + 4
int      i_margin_stopout=30;                        // margin stopout level           //  368 = 0x0170 + 4
int      i_margin_stopout_mode=MARGIN_TYPE_PERCENT;  // margin stopout check mode      //  372 = 0x0174 + 4
double   d_margin_initial=0.0;                       // margin requirements            //  376 = 0x0178 + 8
double   d_margin_maintenance=0.0;                                                     //  384 = 0x0180 + 8
double   d_margin_hedged=0.0;                                                          //  392 = 0x0188 + 8
double   d_margin_divider=1.0;                                                         //  400 = 0x0190 + 8
string   s_margin_currency;                          // 12 bytes                       //  408 = 0x0198 + 12
//---- commissions calculation                                                         -------
//++++ add 4 bytes to align the next double                                            +++++++
double   d_comm_base=0.0;                            // basic commission               //  424 = 0x01A8 + 8
int      i_comm_type=COMM_TYPE_PIPS;                 // basic commission type          //  432 = 0x01B0 + 4
int      i_comm_lots=COMMISSION_PER_LOT;             // commission per lot or per deal //  436 = 0x01B4 + 4
//---- for internal use                                                                -------
int      i_from_bar=0;                               // 'fromdate' bar number          //  440 = 0x01B8 + 4
int      i_to_bar=0;                                 // 'todate' bar number            //  444 = 0x01BC + 4
int      i_start_period[6];                                                            //  448 = 0x01C0 + 24
int      i_from=0;                                   // must be zero                   //  472 = 0x01D8 + 4
int      i_to=0;                                     // must be zero                   //  476 = 0x01DC + 4
int      i_freeze_level=0;                           // order's freeze level in points //  480 = 0x01E0 + 4
int      i_reserved[61];                             // unused                         //  484 = 0x01E4 + 244 = 600

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void WriteHeader(int handle,string symbol,int period,int start_bar, int spread, double commissionPips = 0, double commissionMoney = 0, int leverage = 100)
  {
//---- FXT file header
   s_server = AccountServer();
   d_comm_base = commissionPips;
   if (commissionMoney > 0) {
      i_comm_type = COMM_TYPE_MONEY;
      d_comm_base = commissionMoney;
   }
   i_leverage = leverage;
   
   s_symbol=symbol;
   i_period=period;
   i_bars=0;
   s_currency=StringSubstr(s_symbol,0,3);
   s_margin_currency=AccountCurrency();
   string s_c1 = s_currency;
   if (s_currency == "XAU" || s_currency == "XAG") s_currency = StringSubstr(s_symbol,3,3); // fix issue with XAU/XAG calculation
   string s_testpair1 = s_currency + AccountCurrency() + StringSubstr(s_symbol, 6);
   string s_testpair2 = AccountCurrency() + s_currency + StringSubstr(s_symbol, 6);
   if (!(s_currency == AccountCurrency() ||
       MarketInfo(s_testpair1, MODE_BID) > 0 ||
       MarketInfo(s_testpair2, MODE_BID) > 0)) {
       s_currency = AccountCurrency(); // fix issue with symbols other than currency pairs
   }
   int marginCalcMode = (int)MarketInfo(s_symbol, MODE_MARGINCALCMODE);
   double tentative_margin_divider = 0;
   switch (marginCalcMode) {
      case MARGIN_CALC_CFD:
      case MARGIN_CALC_FUTURES:
      case MARGIN_CALC_CFDINDEX:
         s_margin_currency = "USD";
         tentative_margin_divider = MarketInfo(s_symbol, MODE_BID) * MarketInfo(s_symbol,MODE_LOTSIZE) / MarketInfo(s_symbol, MODE_MARGINREQUIRED);
         if (tentative_margin_divider < 0.97 || tentative_margin_divider > 1.03) {
            d_margin_divider = NormalizeDouble(tentative_margin_divider, 0);
         }
         break;
      case MARGIN_CALC_FOREX:
         d_margin_divider = 1;
         s_margin_currency = s_c1;
         break;
   }
   if (spread > 0) {
      i_spread=spread;
   }
   else {
      i_spread=(int)MarketInfo(s_symbol,MODE_SPREAD);
   }
   i_digits=Digits;
   d_point=Point;
   i_lot_min=(int)(MarketInfo(s_symbol,MODE_MINLOT)*100);
   i_lot_max=(int)(MarketInfo(s_symbol,MODE_MAXLOT)*100);
   i_lot_step=(int)(MarketInfo(s_symbol,MODE_LOTSTEP)*100);
   i_stops_level=(int)MarketInfo(s_symbol,MODE_STOPLEVEL);
   d_contract_size=MarketInfo(s_symbol,MODE_LOTSIZE);
   d_tick_value=MarketInfo(s_symbol,MODE_TICKVALUE);
   d_tick_size=MarketInfo(s_symbol,MODE_TICKSIZE);
   i_profit_mode=(int)MarketInfo(s_symbol,MODE_PROFITCALCMODE);
   i_swap_type=(int)MarketInfo(s_symbol,MODE_SWAPTYPE);
   d_swap_long=MarketInfo(s_symbol,MODE_SWAPLONG);
   d_swap_short=MarketInfo(s_symbol,MODE_SWAPSHORT);
   i_free_margin_mode=AccountFreeMarginMode();
   i_margin_mode=(int)MarketInfo(s_symbol,MODE_MARGINCALCMODE);
   i_margin_stopout=AccountStopoutLevel();
   i_margin_stopout_mode=AccountStopoutMode();
   d_margin_initial=MarketInfo(s_symbol,MODE_MARGININIT);
   d_margin_maintenance=MarketInfo(s_symbol,MODE_MARGINMAINTENANCE);
   d_margin_hedged=MarketInfo(s_symbol,MODE_MARGINHEDGED);
   i_from_bar=start_bar;
   i_start_period[0]=1;
   i_freeze_level=(int)MarketInfo(s_symbol,MODE_FREEZELEVEL);
//----
   FileWriteInteger(handle, i_version);
   FileWriteString(handle, s_copyright, 64);
   FileWriteString(handle, s_server, 128);
   FileWriteString(handle, s_symbol, 12);
   FileWriteInteger(handle, i_period);
   FileWriteInteger(handle, i_model);
   FileWriteInteger(handle, i_bars);
   FileWriteInteger(handle, (uint)t_fromdate);
   FileWriteInteger(handle, (uint)t_todate);
   FileWriteInteger(handle, 0);                // alignment to 8 bytes
   FileWriteDouble(handle, d_modelquality);
   FileWriteString(handle, s_currency, 12);
   FileWriteInteger(handle, i_spread);
   FileWriteInteger(handle, i_digits);
   FileWriteInteger(handle, 0);                // alignment to 8 bytes
   FileWriteDouble(handle, d_point);
   FileWriteInteger(handle, i_lot_min);
   FileWriteInteger(handle, i_lot_max);
   FileWriteInteger(handle, i_lot_step);
   FileWriteInteger(handle, i_stops_level);
   FileWriteInteger(handle, b_gtc_pendings);
   FileWriteInteger(handle, 0);                // alignment to 8 bytes
   FileWriteDouble(handle, d_contract_size);
   FileWriteDouble(handle, d_tick_value);
   FileWriteDouble(handle, d_tick_size);
   FileWriteInteger(handle, i_profit_mode);
   FileWriteInteger(handle, b_swap_enable);
   FileWriteInteger(handle, i_swap_type);
   FileWriteInteger(handle, 0);                // alignment to 8 bytes
   FileWriteDouble(handle, d_swap_long);
   FileWriteDouble(handle, d_swap_short);
   FileWriteInteger(handle, i_swap_rollover3days);
   FileWriteInteger(handle, i_leverage);
   FileWriteInteger(handle, i_free_margin_mode);
   FileWriteInteger(handle, i_margin_mode);
   FileWriteInteger(handle, i_margin_stopout);
   FileWriteInteger(handle, i_margin_stopout_mode);
   FileWriteDouble(handle, d_margin_initial);
   FileWriteDouble(handle, d_margin_maintenance);
   FileWriteDouble(handle, d_margin_hedged);
   FileWriteDouble(handle, d_margin_divider);
   FileWriteString(handle, s_margin_currency, 12);
   FileWriteInteger(handle, 0);                // alignment to 8 bytes
   FileWriteDouble(handle, d_comm_base);
   FileWriteInteger(handle, i_comm_type);
   FileWriteInteger(handle, i_comm_lots);
   FileWriteInteger(handle, i_from_bar);
   FileWriteInteger(handle, i_to_bar);
   FileWriteArray(handle, i_start_period, 0, 6);
   FileWriteInteger(handle, i_from);
   FileWriteInteger(handle, i_to);
   FileWriteInteger(handle, i_freeze_level);
   FileWriteArray(handle, i_reserved, 0, 61);
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool ReadAndCheckHeader(int handle,int period,int& bars)
  {
   int    ivalue;
   double dvalue;
   string svalue;
//----
   GetLastError();
   FileFlush(handle);
   FileSeek(handle,0,SEEK_SET);
//----
   if(FileReadInteger(handle,LONG_VALUE)!=FXT_VERSION) return(false);
   FileSeek(handle, 64, SEEK_CUR);
   if(FileReadString(handle, 12)!=Symbol())            return(false);
   if(FileReadInteger(handle)!=period)     return(false);
//---- every tick model
   if(FileReadInteger(handle)!=0)          return(false);
//---- bars
   ivalue=FileReadInteger(handle);
   if(ivalue<=0)                                       return(false);
   bars=ivalue;
//---- model quality
   FileSeek(handle, 12, SEEK_CUR);
   dvalue=FileReadDouble(handle);
   if(dvalue<0.0 || dvalue>100.0)                      return(false);
//---- currency
   svalue=FileReadString(handle, 12);
   if(svalue!=StringSubstr(Symbol(),0,3))              return(false);
//---- spread digits and point
   if(FileReadInteger(handle)<0)           return(false);
   if(FileReadInteger(handle)!=Digits)     return(false);
   FileSeek(handle, 4, SEEK_CUR);
   if(FileReadDouble(handle)!=Point)     return(false);
//---- lot min
   if(FileReadInteger(handle)<0)           return(false);
//---- lot max
   if(FileReadInteger(handle)<0)           return(false);
//---- lot step
   if(FileReadInteger(handle)<0)           return(false);
//---- stops level
   if(FileReadInteger(handle)<0)           return(false);
//---- contract size
   FileSeek(handle, 8, SEEK_CUR);
   if(FileReadDouble(handle)<0.0)        return(false);
//---- profit mode
   FileSeek(handle, 16, SEEK_CUR);
   ivalue=FileReadInteger(handle);
   if(ivalue<0 || ivalue>PROFIT_CALC_FUTURES)          return(false);
//---- triple rollovers
   FileSeek(handle, 28, SEEK_CUR);
   ivalue=FileReadInteger(handle);
   if(ivalue<0 || ivalue>6)                            return(false);
//---- leverage
   ivalue=FileReadInteger(handle);
   if(ivalue<=0 || ivalue>500)                         return(false);
//---- unexpected end of file
   if(GetLastError()==4099)                            return(false);
//---- check for stored bars
   if((int)FileSize(handle)<600+bars*52)                    return(false);
//----
   return(true);
  }
//+------------------------------------------------------------------+

