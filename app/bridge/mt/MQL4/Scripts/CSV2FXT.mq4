/*
    Copyright (C) 2009-2012 Birt Ltd <birt@eareview.net>

    This license governs use of the accompanying software. If you use the software, you accept this license. If you do not accept the license, do not use the software.
    
    1. Definitions

    The terms "reproduce", "reproduction", and "distribution" have the same meaning here as under U.S. copyright law.
    "You" means the licensee of the software, who is not engaged in designing, developing, or testing other software that has the same or substantially the same features or functionality as the software.
    "Your company" means the company you worked for when you downloaded the software.
    "Reference use" means use of the software within your company as a reference, in read only form, for the sole purposes of debugging and maintaining your products to run properly in conjuction with the software. For clarity, "reference use" does NOT include (a) the right to use the software for purposes of designing, developing, or testing other software that has the same or substantially the same features or functionality as the software, and (b) the right to distribute the software outside of your household or company.
    "Licensed patents" means any Licensor patent claims which read directly on the software as distributed by the Licensor under this license.
    
    2. Grant of Rights

    (A) Copyright Grant- Subject to the terms of this license, the Licensor grants you a non-transferable, non-exclusive, worldwide, royalty-free copyright license to use and to reproduce the software for reference use.
    (B) Patent Grant- Subject to the terms of this license, the Licensor grants you a non-transferable, non-exclusive, worldwide, royalty-free patent license under licensed patents for reference use.
    
    3. Limitations

    (A) No Trademark License- This license does not grant you any rights to use the Licensor's name, logo, or trademarks.
    (B) If you begin patent litigation against the Licensor over patents that you think may apply to the software (including a cross-claim or counterclaim in a lawsuit), your license to the software ends automatically.
    (C) The software is licensed "as-is." You bear the risk of using it. The Licensor gives no express warranties, guarantees or conditions. You may have additional consumer rights under your local laws which this license cannot change. To the extent permitted under your local laws, the Licensor excludes the implied warranties of merchantability, fitness for a particular purpose and non-infringement.
*/
#property copyright "birt"
#property link      "http://eareview.net/"
#property show_inputs
#property strict

#define FILE_ATTRIBUTE_READONLY 1
#define GENERIC_READ -2147483648
#define OPEN_EXISTING 3
#define W_FILE_SHARE_READ 1
#define FILE_ATTRIBUTE_NORMAL 128
#define FILE_START 0
#define FILE_END 2
#define MAX_PATH 260
#define MB_ICONQUESTION 0x00000020
#define MB_ICONEXCLAMATION 0x00000030
#define MB_ICONSTOP 0x00000010
#define MB_YESNO 0x00000004
#define IDYES 6
#define INVALID_FILE_ATTRIBUTES -1
#define MOVEFILE_REPLACE_EXISTING 1

#define DLL_VERSION "0, 0, 1, 2"
#define DLL_NAME "CsvReader.dll"

#import "kernel32.dll"
   int  SetFileAttributesW(string file, int attributes);
   int  GetFileAttributesW(string file);
   int  CreateFileW(string lpFileName, int dwDesiredAccess, int dwShareMode, int lpSecurityAttributes, int dwCreationDisposition, int dwFlagsAndAttributes, int hTemplateFile);
   int  GetFileSize(int hFile, int& lpFileSizeHigh[]);
   int  SetFilePointer(int hFile, int lDistanceToMove, int& lpDistanceToMoveHigh[], int dwMoveMethod);
   int  ReadFile(int hFile, int &lpBuffer[], int nNumberOfBytesToRead, int &lpNumberOfBytesRead[], int lpOverlapped);
   int  CloseHandle(int hObject);
   int  MoveFileExW(string lpExistingFileName, string lpNewFileName, int dwFlags);
#import "Version.dll"
   int  GetFileVersionInfoSizeW(string lptstrFilename, int lpdwHandle);
   bool GetFileVersionInfoW(string lptstrFilename, int dwHandle, int dwLen, int& lpData[]);
#import DLL_NAME
   int    CsvOpen(string fileName, int delimiter);
   string CsvReadString(int fd);
   double CsvReadDouble(int fd);
   int    CsvIsLineEnding(int fd);
   int    CsvIsEnding(int fd);
   int    CsvClose(int fd);
   int    CsvSeek(int fd, int offset, int origin);
#import

enum Version {
   CSV2FXT_Version=0, // 0.50
};

enum DST {
   NO_DST=0,   // None
   US_DST=1,   // US DST
   EU_DST=2,   // European DST
   RU_DST=3,   // Russian DST
   AU_AEDT=4   // Australian AEDT
};

enum GMT {
   GMT_M12=-12,   // GMT-12
   GMT_M11=-11,   // GMT-11
   GMT_M10=-10,   // GMT-10
   GMT_M09=-9,    // GMT-09
   GMT_M08=-8,    // GMT-08
   GMT_M07=-7,    // GMT-07
   GMT_M06=-6,    // GMT-06
   GMT_M05=-5,    // GMT-05
   GMT_M04=-4,    // GMT-04
   GMT_M03=-3,    // GMT-03
   GMT_M02=-2,    // GMT-02
   GMT_M01=-1,    // GMT-01
   GMT_P00=0,     // GMT+00
   GMT_P01=1,     // GMT+01
   GMT_P02=2,     // GMT+02
   GMT_P03=3,     // GMT+03
   GMT_P04=4,     // GMT+04
   GMT_P05=5,     // GMT+05
   GMT_P06=6,     // GMT+06
   GMT_P07=7,     // GMT+07
   GMT_P08=8,     // GMT+08
   GMT_P09=9,     // GMT+09
   GMT_P10=10,    // GMT+10
   GMT_P11=11,    // GMT+11
   GMT_P12=12,    // GMT+12
};

enum ADST {
   AUTO_DST=-1, // Autodetect
   ANO_DST=0,   // None
   AUS_DST=1,   // US DST
   AEU_DST=2,   // European DST
   ARU_DST=3,   // Russian DST
   AAU_AEDT=4   // Australian AEDT
};

enum AGMT {
   AGMT_M12=-12,   // GMT-12
   AGMT_M11=-11,   // GMT-11
   AGMT_M10=-10,   // GMT-10
   AGMT_M09=-9,    // GMT-09
   AGMT_M08=-8,    // GMT-08
   AGMT_M07=-7,    // GMT-07
   AGMT_M06=-6,    // GMT-06
   AGMT_M05=-5,    // GMT-05
   AGMT_M04=-4,    // GMT-04
   AGMT_M03=-3,    // GMT-03
   AGMT_M02=-2,    // GMT-02
   AGMT_M01=-1,    // GMT-01
   AGMT_AUTO=-13,  // Autodetect
   AGMT_P00=0,     // GMT+00
   AGMT_P01=1,     // GMT+01
   AGMT_P02=2,     // GMT+02
   AGMT_P03=3,     // GMT+03
   AGMT_P04=4,     // GMT+04
   AGMT_P05=5,     // GMT+05
   AGMT_P06=6,     // GMT+06
   AGMT_P07=7,     // GMT+07
   AGMT_P08=8,     // GMT+08
   AGMT_P09=9,     // GMT+09
   AGMT_P10=10,    // GMT+10
   AGMT_P11=11,    // GMT+11
   AGMT_P12=12,    // GMT+12
};

#include <FXTHeader.mqh>
input Version CSV2FXT_version=0; // CSV2FXT version
extern string CsvFile="";     // CSV filename
extern bool   CreateHst=true; // Create HST files
extern string ValueInfo="(regardless of the number of digits)."; // All spreads & commissions are in pips
extern double Spread = 0.0;
extern string DateInfo1="By default, the whole CSV will be processed."; // Date range info
extern datetime StartDate=0; // Start date
extern datetime EndDate=0; // End date
extern bool   UseRealSpread=false; // Use real (variable) spread
extern double SpreadPadding = 0.0; // Spread padding
extern double MinSpread = 0.0; // Minimum spread
extern string CommissionInfo = "Only fill in the desired commission type."; // Commission info�
extern double PipsCommission = 0.0; // Commission in pips
extern double MoneyCommission = 0.0; // Commission in account currency
extern string Leverage = "automatic (current account leverage)";
extern string GMTOffsetInfo2 = "These apply to the resulting FXT file."; // FXT GMT and DST info
input  GMT    FXTGMTOffset = 0; // FXT GMT offset
input  DST    FXTDST = 0; // FXT DST setting
extern string GMTOffsetInfo3 = "These specify the configuration of the CSV data file."; // CSV GMT and DST info �
input  AGMT   CSVGMTOffset = -13; // CSV GMT offset
input  ADST   CSVDST = -1; // CSV DST setting
extern bool   RemoveDuplicateTicks = true; // Remove duplicate ticks
extern bool   CreateM1 = false; // Create M1 FXT
extern bool   CreateM5 = false; // Create M5 FXT
extern bool   CreateM15 = false; // Create M15 FXT
extern bool   CreateM30 = false; // Create M30 FXT
extern bool   CreateH1 = false; // Create H1 FXT
extern bool   CreateH4 = false; // Create H4 FXT
extern bool   CreateD1 = false; // Create D1 FXT
extern string TimeShiftInfo = "Do not enable unless you know exactly what you're doing."; // Time shift info
extern bool   TimeShift = false; // Time shift
extern double PriceFactor = 1.0; // Price multiplication factor
// this was removed from the externs because mostly nobody needs it
//extern string VolumeInfo1="Only enable this if you actually need it.";
bool UseRealVolume=false;

int      ExtSrcGMT = 0;
int      ExtSrcDST = 0;

int      ExtPeriods[9] = { 1, 5, 15, 30, 60, 240, 1440, 10080, 43200 };
int      ExtPeriodCount = 9;
int      ExtPeriodSeconds[9];
int      ExtHstHandle[9];
int      ExtFxtHandle[9];
bool     ExtPeriodSelection[9] = { false, false, false, false, false, false, false, false, false };

datetime start_date=0;
datetime end_date=0;

int      ExtTicks;
int      ExtBars[9];
int      ExtCsvHandle=-1;
datetime ExtLastTime;
datetime ExtLastBarTime[9];
double   ExtLastOpen[9];
double   ExtLastLow[9];
double   ExtLastHigh[9];
double   ExtLastClose[9];
int      ExtLastVolume[9];
double   ExtSpread;

datetime ExtStartTick = 0;
datetime ExtEndTick = 0;
int      ExtLastYear = 0;

int      ExtCsvDelimiter = 0;
string   ExtFolder = "";
string   ExtTerminalPath = "";

int      ExtFieldTypes[];
int      ExtFieldCount;
int      ExtDateField = -1;
int      ExtDateFormat = -1;
ushort   ExtDateSeparator = 0;
int      ExtBidField1 = -1;
bool     ExtBidField1SpecialCase = false; // only useful for code visual indication
int      ExtBidField2 = -1;
int      ExtAskField1 = -1;
bool     ExtAskField1SpecialCase = false;
int      ExtAskField2 = -1;
int      ExtVolumeBidField = -1;
bool     ExtVolumeBidFieldSpecialCase = true;
int      ExtVolumeAskField = -1;
bool     ExtVolumeAskFieldSpecialCase = true;
double   ExtVolumeDivide = false;
double   ExtTickMaxDifference = 0.1; // if there's more than 10% between ticks, something is definitely wrong

datetime ExtFirstDate = 0;
datetime ExtLastDate = 0;

int      ExtMinHoursGap = 2;

#define FIELD_TYPE_STRING 0
#define FIELD_TYPE_NUMBER 1
#define KNOWN_DATE_FORMATS 20

void OnDeinit(const int reason) {

}

void OnStart()
  {
   if (!IsDllsAllowed()) {
      string error = "DLL calls are not allowed! They need to be enabled for this script to run (go to Tools->Options->Expert Advisors, enable Allow DLL calls and disable Confirm DLL calls).";
      MessageBox(error, "CSV2FXT", MB_ICONSTOP);
      Print(error);
      return;
   }
   ExtTerminalPath = TerminalInfoString(TERMINAL_DATA_PATH) + "\\";
   ExtFolder = ExtTerminalPath + "MQL4\\Files\\";
   int fd = CreateFileW(ExtTerminalPath + "\\MQL4\\Libraries\\" + DLL_NAME, GENERIC_READ, W_FILE_SHARE_READ, 0, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0);
   if (fd < 0) {
      string error = "The DLL file appears to be missing. Please place it in the correct location and restart the script.";
      Alert(error);
      Print(error);
      return;
   }
   CloseHandle(fd);
   if (StringCompare(DllVersion(DLL_NAME), DLL_VERSION) != 0) {
      string error = "You are not using the correct DLL file. Please replace it and restart the script.";
      MessageBox(error, "CSV2FXT", MB_ICONSTOP);
      Print(error);
      return;
   }
   int i;
   for(int try=0; try<5; try++) if (IsConnected()) break; else Sleep(3000);
   if (!IsConnected()) {
      string error = "This script requires a connection to the broker. Please restart it after MT4 is connected.";
      MessageBox(error, "CSV2FXT", MB_ICONSTOP);
      Print(error);
      return;
   }
   if (HasExtraDigit()) {
      Spread *= 10;
      SpreadPadding *= 10;
      MinSpread *= 10;
   }
   else {
      Spread = NormalizeDouble(Spread, 0);
      SpreadPadding = NormalizeDouble(SpreadPadding, 0);
   }
   if (UseRealSpread) {
      UseRealVolume = false;
   }
   for (i = 0; i < ExtPeriodCount; i++) {
      if (ExtPeriods[i] == Period()) {
         ExtPeriodSelection[i] = true;
         break;
      }
   }
   int LeverageVal = AccountLeverage();
   if (IsNumeric(Leverage)) {
      LeverageVal = StrToInteger(Leverage);
   }
   
   if(CreateM1 == true) ExtPeriodSelection[0] = true;
   if(CreateM5 == true) ExtPeriodSelection[1] = true;
   if(CreateM15 == true) ExtPeriodSelection[2] = true;
   if(CreateM30 == true) ExtPeriodSelection[3] = true;
   if(CreateH1 == true) ExtPeriodSelection[4] = true;
   if(CreateH4 == true) ExtPeriodSelection[5] = true;
   if(CreateD1 == true) ExtPeriodSelection[6] = true;
   
   if (CsvFile == "") {
      CsvFile = StringSubstr(Symbol(),0,6) + ".csv";
   }
   ExtCsvHandle=FileOpen(CsvFile,FILE_CSV|FILE_READ,',');
   if(ExtCsvHandle<0) {
      string error = "Can\'t open input file " + CsvFile;
      MessageBox(error, "CSV2FXT", MB_ICONSTOP);
      Print(error);
      return;
   }
   FileClose(ExtCsvHandle);
   if (!UseRealSpread && Spread == 0) {
      if (TimeDayOfWeek(TimeLocal()) == 0 || TimeDayOfWeek(TimeLocal()) == 6) {
         double currentSpread = Ask - Bid;
         double point = Point;
         if (HasExtraDigit()) {
            point *= 10;
         }
         currentSpread /= point;
         int response = MessageBox("You are building an FXT file with fixed spread using the current broker spread (" + DoubleToStr(currentSpread, 1) + " pips) during the weekend. Are you sure you want to proceed?", "Spread warning", MB_YESNO | MB_ICONQUESTION);
         if (response != IDYES) {
            return;
         }
      }
   }
   if (StartDate > 0) {
      start_date = StartDate;
   }
   if (EndDate > 0) {
      end_date = EndDate;
   }
   if (!FigureOutCSVFormat(CsvFile)) {
      string error = "Bad CSV format. Aborting.";
      MessageBox(error, "CSV2FXT", MB_ICONSTOP);
      Print(error);
      return;
   }
   datetime cur_time,cur_open;
   double   tick_price;
   double   tick_volume;
//----
   ExtTicks = 0;
   ExtLastTime=0;
//---- open input csv-file
   ExtCsvHandle=CsvOpen(ExtFolder + CsvFile, ExtCsvDelimiter);
   if (ExtCsvHandle < 0) {
      MessageBox("Error opening CSV file. Aborting.", "CSV2FXT", MB_ICONSTOP);
      return;
   }
//---- open output fxt files
   if (!OpenFxtFiles()) {
      MessageBox("Unable to open any of the FXT files. Aborting.", "CSV2FXT", MB_ICONSTOP);
      return;
   }
//----
   for (i = 0; i < ExtPeriodCount; i++) {
      ExtPeriodSeconds[i] = ExtPeriods[i] * 60;
      ExtBars[i]=0;
      ExtLastBarTime[i]=0;
   }
   if (HasExtraDigit()) {
      PipsCommission *= 10;
   }
   for (i = 0; i < ExtPeriodCount; i++) {
      if (ExtPeriodSelection[i]) {
         WriteHeader(ExtFxtHandle[i],Symbol(),ExtPeriods[i],0,(int)Spread,PipsCommission,MoneyCommission,LeverageVal);
      }
   }
//---- open hst-files and write their headers
   if(CreateHst) WriteHstHeaders();
   int progress = -1;
   if (ExtLastDate != 0) {
      ObjectCreate("csv2fxt-label",OBJ_LABEL,0,0,0,0,0);
      ObjectSet("csv2fxt-label",OBJPROP_XDISTANCE,30);
      ObjectSet("csv2fxt-label",OBJPROP_YDISTANCE,30);
   }
   double span = (double)ExtLastDate - (double)ExtFirstDate;
   datetime firstTick = 0;
//---- csv read loop
   while(!IsStopped())
     {
      //---- if end of file reached exit from loop
      bool hasMoreRecords = ReadNextTick(cur_time,tick_price,tick_volume);
      if (ExtLastDate != 0) {
         if (firstTick == 0) firstTick = cur_time;
         double currentProgress = ((double)cur_time - (double)firstTick);
         currentProgress /= span;
         currentProgress *= 100;
         if (ExtLastDate != 0 &&
             currentProgress >= progress + 1) {
             progress = (int)MathFloor(currentProgress);
             ObjectSetText("csv2fxt-label", (string)progress + "%",16,"Tahoma",Gold);
             WindowRedraw();
         }
      }
      if (TimeYear(cur_time) != ExtLastYear) {
         ExtLastYear = TimeYear(cur_time);
         Print("Starting to process " + Symbol() + " " + (string)ExtLastYear + ".");
      }
      for (i = 0; i < ExtPeriodCount; i++) {
       //---- calculate bar open time from tick time
       cur_open=cur_time/ExtPeriodSeconds[i];
       cur_open*=ExtPeriodSeconds[i];
       //---- new bar?
       bool newBar = false;
       if (i < 7) {
         if(ExtLastBarTime[i]!=cur_open) {
            newBar = true;
         }
       }
       else if (i == 7) {
         // weekly timeframe
         if (cur_time - ExtLastBarTime[i] >= ExtPeriodSeconds[i]) {
            newBar = true;
         }
         if (newBar) {
            cur_open = cur_time;
            cur_open -= cur_open % (1440 * 60);
            while (TimeDayOfWeek(cur_open) != 0) {
               cur_open -= 1440 * 60;
            }
         }
       }
       else if (i == 8) {
         // monthly timeframe
         if (ExtLastBarTime[i] == 0) {
            newBar = true;
         }
         if (TimeDay(cur_time) < 5 && (cur_time - ExtLastBarTime[i] > 10 * 1440 * 60)) {
            newBar = true;
         }
         if (newBar) {
            cur_open = cur_time;
            cur_open -= cur_open % (1440 * 60);
            while (TimeDay(cur_open) != 1) {
               cur_open -= 1440 * 60;
            }
         }
       }
       if(newBar)
         {
          if(ExtBars[i]>0) {
            WriteBar(i);
            if (i == 0) { // fill in flat the M1 bars if there was no tick for several minutes
              datetime diff = (cur_open - ExtLastBarTime[i]) / ExtPeriodSeconds[i];
              if (diff > 1 && diff < 5) {
                 datetime tempLastBarTime = ExtLastBarTime[i];
                 ExtLastLow[i] = ExtLastClose[i];
                 ExtLastHigh[i] = ExtLastClose[i];
                 ExtLastOpen[i] = ExtLastClose[i];
                 ExtLastVolume[i] = 0;
                 for (int k = 1; k < diff; k++) {
                    ExtLastBarTime[i] = tempLastBarTime + k * ExtPeriodSeconds[i];
                    WriteBar(i);
                    ExtBars[i]++;
                 }
              }
            }
          }
          ExtLastBarTime[i]=cur_open;
          ExtLastOpen[i]=tick_price;
          ExtLastLow[i]=tick_price;
          ExtLastHigh[i]=tick_price;
          ExtLastClose[i]=tick_price;
          if (tick_volume > 0) {
            ExtLastVolume[i]=(int)tick_volume;
          }
          else {
            ExtLastVolume[i]=1;
          }
          ExtBars[i]++;
         }
       else
         {
          //---- check for minimum and maximum
          if(ExtLastLow[i]>tick_price)  ExtLastLow[i]=tick_price;
          if(ExtLastHigh[i]<tick_price) ExtLastHigh[i]=tick_price;
          ExtLastClose[i]=tick_price;
          ExtLastVolume[i]+=(int)tick_volume;
         }
      }

      if (start_date > 0 && cur_time < start_date) continue;
      if (end_date > 0 && cur_time >= end_date) {
        break;
      }
      if (ExtStartTick == 0) ExtStartTick = cur_time;
      ExtEndTick = cur_time;
      WriteTick();
      if(!hasMoreRecords) break;
     }
//---- finalize
   for (i = 0; i < ExtPeriodCount; i++) {
    WriteBar(i);
    if(ExtHstHandle[i]>0) {
      // need to update the last timestamp in the HST header for M1
      FileFlush(ExtHstHandle[i]);
      FileSeek(ExtHstHandle[i],0x58,SEEK_SET);
      FileWriteInteger(ExtFxtHandle[i], (int)ExtLastTime);
      FileClose(ExtHstHandle[i]);
    }
   }
   CsvClose(ExtCsvHandle);
   string fileName;
   for (i = 0; i < ExtPeriodCount; i++) {
      if (ExtPeriodSelection[i]) {
//---- store processed bars amount
         FileFlush(ExtFxtHandle[i]);
         FileSeek(ExtFxtHandle[i],216,SEEK_SET);
         FileWriteInteger(ExtFxtHandle[i],ExtBars[i]);
         FileWriteInteger(ExtFxtHandle[i],(int)ExtStartTick);
         FileWriteInteger(ExtFxtHandle[i],(int)ExtEndTick);
         FileClose(ExtFxtHandle[i]);
         fileName=Symbol()+(string)ExtPeriods[i]+"_0.fxt";
         SetFileAttributesW(ExtFolder + fileName, FILE_ATTRIBUTE_READONLY);
      }
   }
   Print(ExtTicks," ticks added.");
   if (ExtLastDate != 0) {
      ObjectDelete("csv2fxt-label");
      WindowRedraw();
   }
   string hstFiles = "";
   string note = "";
   if (CreateHst) {
      hstFiles = " and the HST files to history\\" + AccountServer();
      note = "\nNote: this will overwrite any existing " + Symbol() + " HST files in the history\\" + AccountServer() + " folder!";
   }
   if (MessageBox("Processing for " + Symbol() + " has finished.\nWould you like to move the FXT file(s) to tester\\history" + hstFiles + "?" + note, "CSV2FXT", MB_YESNO | MB_ICONQUESTION) == IDYES) {
      for (i = 0; i < ExtPeriodCount; i++) {
         if (ExtPeriodSelection[i] && ExtFxtHandle[i] >= 0) {
            fileName=Symbol()+(string)ExtPeriods[i]+"_0.fxt";
            int attr = GetFileAttributesW(ExtFolder + fileName);
            bool copyOk = false;
            if (attr == INVALID_FILE_ATTRIBUTES) {
               copyOk = true;
            }
            else if ((attr & FILE_ATTRIBUTE_READONLY) != 0) {
               if (MessageBox("File tester\\history\\" + fileName + " already exists and has its readonly attribute set. Would you like to overwrite it?", "CSV2FXT", MB_ICONQUESTION | MB_YESNO) == IDYES) {
                  SetFileAttributesW(ExtTerminalPath + "tester\\history\\" + fileName, FILE_ATTRIBUTE_NORMAL);
                  copyOk = true;
               }
            }
            else {
               copyOk = true;
            }
            if (copyOk) {
               if (MoveFileExW(ExtFolder + fileName, ExtTerminalPath + "\\tester\\history\\" + fileName, MOVEFILE_REPLACE_EXISTING) == 0) {
                  MessageBox("Unable to move MQL4\\Files\\" + fileName + " to " + "tester\\history\\" + fileName + ".", "CSV2FXT", MB_ICONEXCLAMATION);
               }
            }
         }
      }
      if (CreateHst) {
         string targetPath = "history\\" + AccountServer() + "\\";
         for (i = 0; i < ExtPeriodCount; i++) {
            fileName = Symbol() + (string)ExtPeriods[i] + ".hst";
            if (MoveFileExW(ExtFolder + fileName, ExtTerminalPath + targetPath + fileName, MOVEFILE_REPLACE_EXISTING) == 0) {
               MessageBox("Unable to move MQL4\\Files\\" + fileName + " to " + targetPath + fileName + ".");
            }
         }
         MessageBox("You should restart your MT4 terminal at this point to make sure the HST files are properly synchronized.", "CSV2FXT", MB_ICONEXCLAMATION);
      }
   }
//----
   return;
  }

int lastTickTimeMin = -1;
double lastTickBid = 0;
double lastTickAsk = 0;
int extraFieldsMsg = 0;
int wrongPricesMsg = 0;
int gapAlertMsg = 0;

bool OpenFxtFiles() {
   int i;
   for (i = 0; i < ExtPeriodCount; i++) {
      if (ExtPeriodSelection[i]) {
         string fileName=Symbol()+(string)ExtPeriods[i]+"_0.fxt";
         ExtFxtHandle[i]=FileOpen(fileName,FILE_BIN|FILE_WRITE);
         if(ExtFxtHandle[i]<0) {
            int attr = GetFileAttributesW(ExtFolder + fileName);
            if ((attr & FILE_ATTRIBUTE_READONLY) != 0) {
               if (MessageBox("File MQL4\\Files\\" + fileName + " already exists and has its readonly attribute set. Would you like to overwrite it?", "CSV2FXT", MB_ICONQUESTION | MB_YESNO) == IDYES) {
                  SetFileAttributesW(ExtFolder + fileName, FILE_ATTRIBUTE_NORMAL);
                  ExtFxtHandle[i]=FileOpen(fileName,FILE_BIN|FILE_WRITE);
                  if (ExtFxtHandle[i]<0) {
                     MessageBox("Was unable to open MQL4\\Files\\" + fileName + " even after removing its readonly attribute. Proceeding with any others.", "CSV2FXT", MB_ICONEXCLAMATION);
                  }
               }
            }
            else {
               MessageBox("Unable to open MQL4\\Files\\" + fileName + ". Proceeding with any others.", "CSV2FXT", MB_ICONEXCLAMATION);
            }
         }
      }
   }
   bool result = false;
   for (i = 0; i < ExtPeriodCount; i++) {
      if (ExtPeriodSelection[i] && ExtFxtHandle[i] >= 0) {
         result = true;
      }
      else {
         ExtPeriodSelection[i] = false;
      }
   }
   return (result);
}

// Dukascopy custom exported data format:
// yyyy.mm.dd hh:mm:ss,bid,ask,bid_volume,ask_volume
bool ReadNextTick(datetime& cur_time, double& tick_price, double& tick_volume)
  {
  tick_volume = 0;
//----
   bool hadOlderTickError = false;
   while(!IsStopped())
    {
      // read record
      datetime date_time = 0;
      double dblAsk = 0, dblBid = 0, dblAskVol = 0, dblBidVol = 0;
      bool brokenRecord = false;
      for (int i = 0; i < ExtFieldCount; i++) {
         if (ExtFieldTypes[i] == FIELD_TYPE_STRING) {
            string field = CsvReadString(ExtCsvHandle);
            if (ExtDateField == i) {
               if (ParseDate(field, ExtDateFormat, date_time)) {
                  if (date_time == 0) {
                     brokenRecord = true;
                     break;
                  }
               }
               else {
                  brokenRecord = true;
                  break;
               }
            }
            else if (ExtAskField1 == i) {
               dblAsk = SpecialStrToDouble(field);
               if (dblAsk == 0) {
                  brokenRecord = true;
                  break;
               }
            }
            else if (ExtBidField1 == i) {
               dblBid = SpecialStrToDouble(field);
               if (dblBid == 0) {
                  brokenRecord = true;
                  break;
               }
            }
             else if (ExtVolumeAskField == i) {
                dblAskVol = SpecialStrToDouble(field);
             }
             else if (ExtVolumeBidField == i) {
                dblBidVol = SpecialStrToDouble(field);
             }
         }
         else {
            double value = CsvReadDouble(ExtCsvHandle);
             if (ExtAskField1 == i) {
               if (value == 0) {
                  brokenRecord = true;
                  break;
               }
                dblAsk = value;
             }
             else if (ExtBidField1 == i) {
               if (value == 0) {
                  brokenRecord = true;
                  break;
               }
                dblBid = value;
             }
             else if (ExtAskField2 == i) {
                dblAsk += MakeFractional(DoubleToStr(value, 0));
             }
             else if (ExtBidField2 == i) {
                dblBid += MakeFractional(DoubleToStr(value, 0));
             }
             else if (ExtVolumeAskField == i) {
                dblAskVol = value;
             }
             else if (ExtVolumeBidField == i) {
                dblBidVol = value;
             }
          }
       }

       if (!CsvIsEnding(ExtCsvHandle) && !CsvIsLineEnding(ExtCsvHandle) && extraFieldsMsg < 20 &&
            ExtLastTime != 0) { // don't report this if it's the header row
          Print("Extra fields detected & discarded in the CSV file in record after " + TimeToStr(ExtLastTime, TIME_MINUTES|TIME_DATE|TIME_SECONDS));
          extraFieldsMsg++;
          if (extraFieldsMsg >= 20) {
            Print("The extra fields message repeated over 20 times so far. It is now suppressed to avoid cluttering your log files.");
          }
       }

       if (!SkipToNextLine(ExtCsvHandle)) { // in case there are extra fields (broken CSVs), skip to the next record
          // file is ending
          return (false);
       }
       
       if (brokenRecord) {
          if (ExtLastTime != 0) {  // don't report this if it's the header row
            Print("Broken record in the CSV file after " + TimeToStr(ExtLastTime, TIME_MINUTES|TIME_DATE|TIME_SECONDS));
          }
          continue;
       }
       
       dblAsk = NormalizeDouble(PriceFactor * dblAsk, Digits);
       dblBid = NormalizeDouble(PriceFactor * dblBid, Digits);
       
       if (wrongPricesMsg < 20 && ExtLastTime != 0) {
         if ( (lastTickAsk != 0 && MathAbs(dblAsk - lastTickAsk) > lastTickAsk * ExtTickMaxDifference) ||
              (lastTickBid != 0 && MathAbs(dblBid - lastTickBid) > lastTickBid * ExtTickMaxDifference) ||
              MathAbs(dblBid - dblAsk) > lastTickBid * ExtTickMaxDifference) {
           Print("There seems to be something wrong with the prices for the tick at " + TimeToStr(date_time, TIME_MINUTES|TIME_DATE|TIME_SECONDS) + ". Skipping it. Skipped tick ask: " + DoubleToStr(dblAsk, Digits) + ", bid: " + DoubleToStr(dblBid, Digits) + "; previous tick ask: " + DoubleToStr(lastTickAsk, Digits) + ", bid: " + DoubleToStr(lastTickBid, Digits) + ".");
            wrongPricesMsg++;
            if (wrongPricesMsg >= 20) {
              Print("The wrong prices message repeated over 20 times so far. It is now suppressed to avoid cluttering your log files.");
             Alert("Your CSV file for " + Symbol() + " appears to have a lot of damaged prices. You should check the experts log for more information.");
            }
            continue;
         }
      }
      
      date_time -= ExtSrcGMT * 3600;
      date_time -= DSTOffset(cur_time, ExtSrcDST);
      
      cur_time = date_time + FXTGMTOffset * 3600;
      cur_time += DSTOffset(cur_time, FXTDST);
      if (TimeShift) {
         cur_time -= 883612800;
      }
      tick_price = dblBid;
      
      if (UseRealSpread) {
         ExtSpread = NormalizeDouble(dblAsk - tick_price + SpreadPadding * Point, Digits);
         if (ExtSpread < MinSpread * Point) ExtSpread = NormalizeDouble(MinSpread * Point, Digits);
      }
      
      if (!UseRealVolume) {
         tick_volume = 1;
      }
      else {
         tick_volume += dblAskVol / ExtVolumeDivide + dblBidVol / ExtVolumeDivide;
      }
      if (tick_volume <= 0) {
         tick_volume = 1;
      }

      if (RemoveDuplicateTicks) {
         if (TimeMinute(cur_time) == lastTickTimeMin && dblBid == lastTickBid && (!UseRealSpread || dblAsk == lastTickAsk)) continue;
      }
      lastTickTimeMin = TimeMinute(cur_time);
      lastTickAsk = dblAsk;
      lastTickBid = dblBid;
      
      if (ExtLastTime != 0 && cur_time >= ExtLastTime + ExtMinHoursGap * 3600) {
         int day = TimeDayOfWeek(cur_time);
         bool alert = true;
         double gap = ((double)cur_time - (double)ExtLastTime) / (3600);
         if (day == 0 || day == 1) { // Sunday or Monday
            if (gap >= 42 && gap <= 54) { // weekend duration accounting for an early or late market start
               alert = false;
            }
         }
         int curDay = TimeDay(cur_time);
         int curMonth = TimeMonth(cur_time);
         int oldDay = TimeDay(ExtLastTime);
         int oldMonth = TimeMonth(ExtLastTime);
         if (curMonth == 12 && curDay > 24 && curDay < 28 && oldMonth == 12 && oldDay <= 24 && oldDay > 21) { // Christmas, accounting for potential weekend before and after
            alert = false;
         }
         if (curMonth == 1 && curDay < 4 && oldMonth == 12 && oldDay >= 29) { // New year, accounting for potential weekend before and after
            alert = false;
         }
         if (alert) {
            string msg = "Possible " + Symbol() + " error: gap after " + TimeToStr(ExtLastTime, TIME_MINUTES|TIME_DATE|TIME_SECONDS) + " (" + DoubleToStr(gap, 1) + " hours).";
            if (gapAlertMsg < 5) {
               Alert(msg);
            }
            gapAlertMsg++;
            Print(msg);
            if (gapAlertMsg == 5) {
               Print("There were 5 gap errors so far. Since your CSV file is starting to look like Schweizer cheese, alerts are now suppressed.");
            }
         }
      }
      //---- time must go forward. if no then read further
      if(cur_time>=ExtLastTime) break;
      if (!hadOlderTickError) {
         Print("Error in the CSV file: encountered older timestamp(s) right after the tick at " + TimeToStr(ExtLastTime, TIME_DATE|TIME_MINUTES|TIME_SECONDS) + " (older timestamp: " + TimeToStr(cur_time, TIME_DATE|TIME_MINUTES|TIME_SECONDS) + ").");
         hadOlderTickError = TRUE;
      }
   }
   ExtLastTime=cur_time;
   return(true);
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+

void WriteTick()
  {
//---- current bar state
   for (int i = 0; i < ExtPeriodCount; i++) {
      if (ExtPeriodSelection[i]) {
         FileWriteLong(ExtFxtHandle[i], ExtLastBarTime[i]);
         FileWriteDouble(ExtFxtHandle[i], ExtLastOpen[i]);
         FileWriteDouble(ExtFxtHandle[i], ExtLastHigh[i]);
         FileWriteDouble(ExtFxtHandle[i], ExtLastLow[i]);
         FileWriteDouble(ExtFxtHandle[i], ExtLastClose[i]);
         FileWriteInteger(ExtFxtHandle[i], ExtLastVolume[i]);
         if (UseRealSpread) {
            double spread = NormalizeDouble(ExtSpread / Point, 0);
            FileWriteInteger(ExtFxtHandle[i], (int)spread);
         }
         else {
            FileWriteInteger(ExtFxtHandle[i], 0);
         }
//---- incoming tick time
         FileWriteInteger(ExtFxtHandle[i], (int)ExtLastTime);
         FileWriteInteger(ExtFxtHandle[i], 3);
      }
   }
//---- ticks counter
   ExtTicks++;
  }
//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
void WriteHstHeaders()
  {
//---- History header
   for (int i = 0; i < ExtPeriodCount; i++) {
      int    i_hversion=401;
      string c_copyright;
      string c_symbol=Symbol();
      int    i_hperiod=ExtPeriods[i];
      int    i_hdigits=Digits;
      int    i_unused[13];
//----  
      ExtHstHandle[i]=FileOpen(c_symbol+(string)i_hperiod+".hst", FILE_BIN|FILE_WRITE);
      if(ExtHstHandle[i] < 0) Print("Error opening " + c_symbol + (string)i_hperiod + ".hst");
//---- write history file header
      c_copyright="(C)opyright 2003, MetaQuotes Software Corp.";
      FileWriteInteger(ExtHstHandle[i], i_hversion);
      FileWriteString(ExtHstHandle[i], c_copyright, 64);
      FileWriteString(ExtHstHandle[i], c_symbol, 12);
      FileWriteInteger(ExtHstHandle[i], i_hperiod);
      FileWriteInteger(ExtHstHandle[i], i_hdigits);
      FileWriteInteger(ExtHstHandle[i],0);
      FileWriteInteger(ExtHstHandle[i],0);
      FileWriteArray(ExtHstHandle[i], i_unused, 0, 13);
   }
  }
//+------------------------------------------------------------------+
//| write corresponding hst-file                                     |
//+------------------------------------------------------------------+
void WriteBar(int i)
  {
   if(ExtHstHandle[i]>0)
     {
      MqlRates r;
      r.time=ExtLastBarTime[i];
      r.open=ExtLastOpen[i];
      r.low=ExtLastLow[i];
      r.high=ExtLastHigh[i];
      r.close=ExtLastClose[i];
      r.tick_volume=MathMax(1, ExtLastVolume[i]);
      r.spread=0;
      r.real_volume=ExtLastVolume[i];
      FileWriteStruct(ExtHstHandle[i],r);
     }
  }
//+------------------------------------------------------------------+

int DSTOffset(datetime t, int DSTType) {
   if (isDST(t, DSTType)) {
      return (3600);
   }
   return (0);
}

bool isDST(datetime t, int zone = 0) {
   datetime dstStart;
   datetime dstEnd;
   if (zone == 2 || zone == 3) { // Europe & Russia
      if (zone == 3 && t > D'28.03.2011') return (false); // no DST for Russia after 28.03.2011
      dstStart = StrToTime((string)TimeYear(t) + ".03.31 01:00");
      while (TimeDayOfWeek(dstStart) != 0) { // last Sunday of March
         dstStart -= 3600 * 24;
      }
      dstEnd = StrToTime((string)TimeYear(t) + ".10.31 01:00");
      while (TimeDayOfWeek(dstEnd) != 0) { // last Sunday of October
         dstEnd -= 3600 * 24;
      }
      if (t >= dstStart && t < dstEnd) {
         return (true);
      }
      else {
         return (false);
      }
   }
   else if (zone == 1) { // US
      dstStart = StrToTime((string)TimeYear(t) + ".03.01 00:00"); // should be Saturday 21:00 GMT (New York is at GMT-5 and it changes at 2AM) but it doesn't really matter since we have no market during the weekend
      int sundayCount = 0;
      while (true) { // second Sunday of March
         if (TimeDayOfWeek(dstStart) == 0) {
            sundayCount++;
            if (sundayCount == 2) break;
         }
         dstStart += 3600 * 24;
      }
      dstEnd = StrToTime((string)TimeYear(t) + ".11.01 00:00");
      while (TimeDayOfWeek(dstEnd) != 0) { // first Sunday of November
         dstEnd += 3600 * 24;
      }
      if (t >= dstStart && t < dstEnd) {
         return (true);
      }
      else {
         return (false);
      }
   }
   else if (zone == 4) { // Australia
      datetime nonDstStart = StrToTime((string)TimeYear(t) + ".04.01 01:00");
      while (TimeDayOfWeek(nonDstStart) != 0) { // first Sunday of April
         nonDstStart += 3600 * 24;
      }
      datetime nonDstEnd = StrToTime((string)TimeYear(t) + ".10.01 01:00");
      while (TimeDayOfWeek(nonDstEnd) != 0) { // first Sunday of October
         nonDstEnd += 3600 * 24;
      }
      if (t >= nonDstStart && t < nonDstEnd) {
         return (false);
      }
      else {
         return (true);
      }
   }
   return (false);
}


bool FigureOutCSVFormat(string csvFile) {
   if (IsCorrectDelimiter(csvFile, ',')) {
      Print("CSV delimiter: comma (,).");
      ExtCsvDelimiter = ',';
   }
   else if (IsCorrectDelimiter(csvFile, ';')) {
      Print("CSV delimiter: semicolon (;).");
      ExtCsvDelimiter = ';';
   }
   else if (IsCorrectDelimiter(csvFile, '\t')) {
      Print("CSV delimiter: tab.");
      ExtCsvDelimiter = '\t';
   }
   else if (IsCorrectDelimiter(csvFile, '|')) {
      Print("CSV delimiter: pipe.");
      ExtCsvDelimiter = '|';
   }
   else {
      MessageBox("Could not figure out the CSV delimiter.", "CSV2FXT", MB_ICONSTOP);
      return (false);
   }
   int csvHandle = CsvOpen(ExtFolder + csvFile, ExtCsvDelimiter);
   if (csvHandle < 0) {
      MessageBox("Error opening CSV file. Aborting.", "CSV2FXT", MB_ICONSTOP);
      return (false);
   }
   int i = 0;
   SkipToNextLine(csvHandle); // skip a potential header, just in case there are problems with the locale & comma
   while (true) {
      string discarded = CsvReadString(csvHandle);
      i++;
      if (CsvIsLineEnding(csvHandle) == 1) {
         break;
      }
   }
   ExtFieldCount = i;
   ArrayResize(ExtFieldTypes, ExtFieldCount);
   CsvSeek(csvHandle, 0, SEEK_SET);
   string field = CsvReadString(csvHandle);
   if (HasLetters(field)) {
      // 2 possible cases: header line or first field is the pair name
      field = CsvReadString(csvHandle);
      if (HasLetters(field)) {
         // next field is also text, we must be dealing with a header line
         SkipToNextLine(csvHandle);
      }
      else {
         // the first field is the currency pair name, what a waste of space
         CsvSeek(csvHandle, 0, SEEK_SET);
      }
   }
   else {
      CsvSeek(csvHandle, 0, SEEK_SET);
   }
   double price1 = 0, price2 = 0, volume1 = 0, volume2 = 0;
   int price1field1 = -1, price1field2 = -1, price2field1 = -1, price2field2 = -1, volume1field = -1, volume2field = -1;
   bool splitRecord = false;
   bool price1specialCase = false;
   bool price2specialCase = false;
   bool volume1specialCase = false;
   bool volume2specialCase = false;
   bool assignedPrice1 = false;
   bool assignedPrice2 = false;
   bool assignedVolume1 = false;
   bool assignedVolume2 = false;
   bool askFirst = false;
   string firstDate = "";
   int fieldid = 0;
   double value = 0;
   bool hadDot = false;
   while (fieldid < ExtFieldCount) {
      field = CsvReadString(csvHandle);
      if (HasLetters(field)) {
         // we've probably had a header and we're now on line 1 reading the currency pair name or something
         Print ("Column " + (string)fieldid + " appears to be a text field, ignoring it. Sample: " + field);
         ExtFieldTypes[fieldid] = FIELD_TYPE_STRING;
      }
      else if (IsNumeric(field)) {
         Print ("Column " + (string)fieldid + " is a numeric field.");
         ExtFieldTypes[fieldid] = FIELD_TYPE_NUMBER;
         if (HasComma(field)) {
            // we have a special case, the delimiter is not comma and the numbers look like 1,2345
            ExtFieldTypes[fieldid] = FIELD_TYPE_STRING; // have to read it as a string
            if (splitRecord) {
               // cannot have a split record where the second part has a decimal separator
               MessageBox("Comma issues detected, perhaps extra field.", "CSV2FXT", MB_ICONSTOP);
               CsvClose(csvHandle);
               return (false);
            }
            value = SpecialStrToDouble(field);
            if (!assignedPrice1) {
               price1 = value;
               price1specialCase = true;
               assignedPrice1 = true;
               price1field1 = fieldid;
            }
            else if (!assignedPrice2) {
               price2 = value;
               price2specialCase = true;
               assignedPrice2 = true;
               price2field1 = fieldid;
            }
            else if (!assignedVolume1) {
               volume1 = value;
               volume1specialCase = true;
               assignedVolume1 = true;
               volume1field = fieldid;
            }
            else if (!assignedVolume2) {
               volume2 = value;
               volume2specialCase = true;
               assignedVolume2 = true;
               volume2field = fieldid;
            }
         }
         else if (HasDot(field) || hadDot) {
            // looks like a perfectly good numeric value
            hadDot = true;
            if (splitRecord) {
               // cannot have a split record where the second part has a decimal separator
               MessageBox("Comma issues detected, perhaps extra field.", "CSV2FXT", MB_ICONSTOP);
               CsvClose(csvHandle);
               return (false);
            }
            value = StrToDouble(field);
            if (!assignedPrice1) {
               price1 = value;
               assignedPrice1 = true;
               price1field1 = fieldid;
            }
            else if (!assignedPrice2) {
               price2 = value;
               assignedPrice2 = true;
               price2field1 = fieldid;
            }
            else if (!assignedVolume1) {
               volume1 = value;
               assignedVolume1 = true;
               volume1field = fieldid;
            }
            else if (!assignedVolume2) {
               volume2 = value;
               assignedVolume2 = true;
               volume2field = fieldid;
            }
         }
         else {
            // no dot, no comma, must mean that the separator is a comma and the user has a locale with comma as decimal separator
            // or we're dealing with an integer such as the volume
            if (splitRecord) {
               // this one belongs to the previous field
               splitRecord = false;
               value = MakeFractional(field);
               if (!assignedPrice1) {
                  price1 += value;
                  assignedPrice1 = true;
                  price1field2 = fieldid;
               }
               else if (!assignedPrice2) {
                  price2 += value;
                  assignedPrice2 = true;
                  price2field2 = fieldid;
               }
            }
            else {
               value = StrToInteger(field);
               if (!assignedPrice1) {
                  price1 = value;
                  price1field1 = fieldid;
                  if (ExtFieldCount > 5) {
                     splitRecord = true;
                  }
                  else {
                     assignedPrice1 = true;
                  }
               }
               else if (!assignedPrice2) {
                  price2 = value;
                  price2field1 = fieldid;
                  if (ExtFieldCount > 5) {
                     splitRecord = true;
                  }
                  else {
                     assignedPrice2 = true;
                  }
               }
               else if (!assignedVolume1) {
                  volume1 = value;
                  volume1field = fieldid;
                  assignedVolume1 = true;
               }
               else if (!assignedVolume2) {
                  volume2 = value;
                  volume2field = fieldid;
                  assignedVolume2 = true;
               }
            }
         }
      }
      else if (LooksLikeDate(field)) {
         ExtDateField = fieldid;
         firstDate = field;
         Print ("The date column appears to be " + (string)fieldid + ". Sample: " + field);
      }
      fieldid++;
   }
   // sort out the prices
   double askPrice, bidPrice;
   while (price1 == price2) {
      for (i = 0; i < ExtFieldCount; i++) {
         if (ExtFieldTypes[i] == FIELD_TYPE_STRING) {
            field = CsvReadString(csvHandle);
            if (price1field1 == i) {
               price1 = SpecialStrToDouble(field);
            }
            else if (price2field1 == i) {
               price2 = SpecialStrToDouble(field);
            }
         }
         else {
            value = CsvReadDouble(csvHandle);
             if (price1field1 == i) {
                price1 = value;
             }
             else if (price2field1 == i) {
                price2 = value;
             }
             else if (price1field2 == i) {
                price1 += MakeFractional(DoubleToStr(value, 0));
             }
             else if (price2field2 == i) {
                price2 += MakeFractional(DoubleToStr(value, 0));
             }
          }
       }
   }
   if (price1 > price2) {
      // the first price is the ask price
      askFirst = true;
      askPrice = price1;
      bidPrice = price2;
      ExtAskField1 = price1field1;
      ExtAskField2 = price1field2;
      ExtAskField1SpecialCase = price1specialCase;
      ExtBidField1 = price2field1;
      ExtBidField2 = price2field2;
      ExtBidField1SpecialCase = price2specialCase;
   }
   else {
      // the bid price comes first
      askFirst = false;
      bidPrice = price1;
      askPrice = price2;
      ExtBidField1 = price1field1;
      ExtBidField2 = price1field2;
      ExtBidField1SpecialCase = price1specialCase;
      ExtAskField1 = price2field1;
      ExtAskField2 = price2field2;
      ExtAskField1SpecialCase = price2specialCase;
   }
   if (ExtAskField2 >= 0) {
      Print("Ask price columns: " + (string)ExtAskField1 + ", " + (string)ExtAskField2 + ". Sample: " + DoubleToStr(askPrice, Digits));
   }
   else {
      Print("Ask price column: " + (string)ExtAskField1 + ". Sample: " + DoubleToStr(askPrice, Digits));
   }
   if (ExtBidField2 >= 0) {
      Print("Bid price columns: " + (string)ExtBidField1 + ", " + (string)ExtBidField2 + ". Sample: " + DoubleToStr(bidPrice, Digits));
   }
   else {
      Print("Bid price column: " + (string)ExtBidField1 + ". Sample: " + DoubleToStr(bidPrice, Digits));
   }
   if (ExtAskField1 < 0 || ExtBidField1 < 0) {
      MessageBox("Unable to identify the ask & bid columns.", "CSV2FXT", MB_ICONSTOP);
      CsvClose(csvHandle);
      return (false);
   }
   if (volume2field >= 0) {
      // we have 2 volume fields
      Print ("We have two volume columns. Arranging them in the same order as the ask/bid prices.");
      double askVolume, bidVolume;
      if (askFirst) {
         askVolume = volume1;
         bidVolume = volume2;
         ExtVolumeAskField = volume1field;
         ExtVolumeAskFieldSpecialCase = volume1specialCase;
         ExtVolumeBidField = volume2field;
         ExtVolumeBidFieldSpecialCase = volume2specialCase;
      }
      else {
         bidVolume = volume1;
         askVolume = volume2;
         ExtVolumeBidField = volume1field;
         ExtVolumeBidFieldSpecialCase = volume1specialCase;
         ExtVolumeAskField = volume2field;
         ExtVolumeAskFieldSpecialCase = volume2specialCase;
      }
      Print ("Ask volume column: " + (string)ExtVolumeAskField + ". Sample: " + (string)askVolume);
      Print ("Bid volume column: " + (string)ExtVolumeBidField + ". Sample: " + (string)bidVolume);
   }
   else if (volume2field >= 0) {
      ExtVolumeAskField = volume1field;
      ExtVolumeAskFieldSpecialCase = volume1specialCase;
      Print ("Volume column: " + (string)ExtVolumeAskField + ". Sample: " + (string)volume1);
   }
   if (volume1 > 100000) {
      ExtVolumeDivide = 100000;
   }
   else {
      ExtVolumeDivide = 1;
   }
   // figure out the date format
   SkipToNextLine(csvHandle);
   int validFormatsCount = 2;
   int lastValidFormat = -1;
   bool validDateFormats[KNOWN_DATE_FORMATS];
   int day[KNOWN_DATE_FORMATS];
   int month[KNOWN_DATE_FORMATS];
   int year[KNOWN_DATE_FORMATS];
   ArrayFill(day, 0, KNOWN_DATE_FORMATS, 0);
   ArrayFill(month, 0, KNOWN_DATE_FORMATS, 0);
   ArrayFill(year, 0, KNOWN_DATE_FORMATS, 0);
   ArrayFill(validDateFormats, 0, KNOWN_DATE_FORMATS, true);
   while (validFormatsCount > 1) {
      validFormatsCount = 0;
      datetime d;
      fieldid = 0;
      while (fieldid <= ExtDateField) {
         field = CsvReadString(csvHandle);
         fieldid++;
      }
      if (StringLen(field) == 0) break; // empty last line for short files
      for(i = 0; i < KNOWN_DATE_FORMATS; i++) {
         if (validDateFormats[i]) {
            if (ParseDate(field, i, d, true)) {
               int curday = TimeDay(d);
               int curmonth = TimeMonth(d);
               int curyear = TimeYear(d);
               if (month[i] != curmonth && day[i] == curday) {
                  // can't change the month without changing the day
                  validDateFormats[i] = false;
               }
               else if (year[i] != curyear && (month[i] == curmonth || day[i] == curday)) {
                  // can't change the year without changing the month and day
                  validDateFormats[i] = false;
               }
               day[i] = curday;
               month[i] = curmonth;
               year[i] = curyear;
               if (validDateFormats[i]) {
                  validFormatsCount++;
                  lastValidFormat = i;
               }
            }
            else {
               validDateFormats[i] = false;
            }
         }
      }
      if (validFormatsCount == 0) {
         CsvClose(csvHandle);
         MessageBox("Unable to understand date format.", "CSV2FXT", MB_ICONSTOP);
         return (false);
      }
      if (!SkipToNextLine(csvHandle)) {
         break; // break if the file is ending
      }
   }
   if (validFormatsCount > 1) {
      CsvClose(csvHandle);
      MessageBox("Unable to clearly identify the date format. Please use a larger CSV file.", "CSV2FXT", MB_ICONSTOP);
      return (false);
   }
   ExtDateFormat = lastValidFormat;
   ParseDate(firstDate, ExtDateFormat, ExtFirstDate);
   Print("Date format identified: " + DateFormatToStr(ExtDateFormat) + ". Elucidating value: " + field);
   CsvClose(csvHandle);
   // try to figure out the data source
   if (CSVGMTOffset > AGMT_AUTO) {
      ExtSrcGMT = CSVGMTOffset;
   }
   if (CSVDST >= 0) {
      ExtSrcDST = CSVDST;
   }
   if (ExtDateFormat == 8 && ExtDateField == 0 && ExtAskField1 == 1 && ExtBidField1 == 2 && ExtVolumeAskField == 3 && ExtVolumeBidField == 4 && ExtVolumeDivide == 1) {
      // Dukascopy via JForex
      Print("Your tick data source seems to be Dukascopy, downloaded via JForex.");
      if (CSVGMTOffset == AGMT_AUTO) {
         ExtSrcGMT = 0;
      }
      if (CSVDST == AUTO_DST) {
         ExtSrcDST = 0;
      }
   }
   else if (ExtDateField == 0 && ExtAskField1 == 1 && ExtBidField1 == 2 && ExtVolumeAskField == 3 && ExtVolumeBidField == 4 && ExtVolumeDivide == 1 &&
            (ExtDateFormat == 9 || ExtDateFormat == 10)
            ) {
      // Dukascopy via website
      Print("Your tick data source seems to be Dukascopy, downloaded via the dukascopy.com website.");
      if (CSVGMTOffset == AGMT_AUTO) {
         ExtSrcGMT = 0;
      }
      if (CSVDST == AUTO_DST) {
         ExtSrcDST = 0;
      }
   }
   else if (ExtDateFormat == 8 && ExtDateField == 0 && ExtBidField1 == 1 && ExtAskField1 == 2 && ExtVolumeBidField == 3 && ExtVolumeAskField == 4 && ExtVolumeDivide == 100000) {
      // Dukascopy via PHP scripts or Dukascopier
      Print("Your tick data source seems to be Dukascopy, downloaded via PHP scripts or Dukascopier.");
      if (CSVGMTOffset == AGMT_AUTO) {
         ExtSrcGMT = 0;
      }
      if (CSVDST == AUTO_DST) {
         ExtSrcDST = 0;
      }
   }
   else if (ExtDateFormat == 13 && ExtDateField == 0 && ExtVolumeAskField == -1) {
      // Oanda
      Print("Your tick data source seems to be Oanda.");
      if (CSVGMTOffset == AGMT_AUTO) {
         ExtSrcGMT = 0;
      }
      if (CSVDST == AUTO_DST) {
         ExtSrcDST = 0;
      }
   }
   else if (ExtDateFormat == 0 && ExtDateField == 1 && ExtVolumeAskField == -1) {
      // Integral/Pepperstone
      Print("Your tick data source seems to be Integral (TrueFX) or Pepperstone.");
      if (CSVGMTOffset == AGMT_AUTO) {
         ExtSrcGMT = 0;
      }
      if (CSVDST == AUTO_DST) {
         ExtSrcDST = 0;
      }
   }
   else if (ExtDateFormat == 8 && ExtDateField == 1 && ExtVolumeAskField == -1) {
      // MB Trading
      Print("Your tick data source seems to be MB Trading.");
      if (CSVGMTOffset == AGMT_AUTO) {
         ExtSrcGMT = -5;
      }
      if (CSVDST == AUTO_DST) {
         ExtSrcDST = 1;
      }
   }
   else if (ExtDateFormat == 16 && ExtDateField == 0 && ExtBidField1 == 1 && ExtAskField1 == 2) {
      // histdata.com
      Print("Your tick data source seems to be histdata.com.");
      if (CSVGMTOffset == AGMT_AUTO) {
         ExtSrcGMT = -5;
      }
      if (CSVDST == AUTO_DST) {
         ExtSrcDST = 1;
      }
      if (CSVGMTOffset == AGMT_AUTO || CSVDST == AUTO_DST) {
         Alert("For histdata.com tick data you should configure the source GMT & DST parameters manually.");
      }
   }
   if (CSVGMTOffset == AGMT_AUTO || CSVDST == AUTO_DST) {
      string cmt = "Autoconfigured";
      string sep = "";
      if (CSVGMTOffset == AGMT_AUTO) {
         cmt = cmt + " source GMT to " + (string)ExtSrcGMT;
         sep = " and";
      }
      if (CSVDST == AUTO_DST) {
         cmt = cmt + sep + " source DST to " + (string)ExtSrcDST;
      }
      cmt = cmt + ".";
      Print(cmt);
   }
   
   // figure out the last date in the file
   if (IsDllsAllowed()) {
      int fd = CreateFileW(ExtFolder + csvFile, GENERIC_READ, W_FILE_SHARE_READ, 0, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0);
      if (fd >= 0) {
         int bytesread[1];
         bytesread[0] = 0;
         int size = GetFileSize(fd, bytesread);
         if (size >= 0 && size < 256) {
            bytesread[0]--;
            size = -1 - (256 - size);
         } else size -= 256;
         int seek = SetFilePointer(fd, size, bytesread, FILE_START);
         bytesread[0] = 0;
         if (seek == -1) {
            Print("Failed to seek to the end of the file. The progress indicator will not be available.");
         }
         else {
            int arrayBuffer[64];
            if (ReadFile(fd, arrayBuffer, 256, bytesread, 0) != 1) {
               Print("Failed to read the end of the file. The progress indicator will not be available.");
            }
            else {
               string randname = "tmp-" + (string)GetTickCount() + "-" + (string)MathRand() + ".csv";
               int csvEnd = FileOpen(randname, FILE_BIN|FILE_WRITE);
               FileWriteArray(csvEnd, arrayBuffer, 0, bytesread[0] / 4);
               FileClose(csvEnd);
               csvEnd = CsvOpen(ExtFolder + randname, ExtCsvDelimiter);
               if (csvEnd >= 0) {
                  while (SkipToNextLine(csvEnd)) {
                     fieldid = 0;
                     while (fieldid <= ExtDateField) {
                        string fieldcontent = CsvReadString(csvEnd);
                        if (StringLen(fieldcontent) > 0) {
                           field = fieldcontent;
                        }
                        fieldid++;
                     }
                  }
                  if (ParseDate(field, ExtDateFormat, ExtLastDate)) {
                     Print("Last date in file: " + TimeToStr(ExtLastDate, TIME_DATE|TIME_MINUTES|TIME_SECONDS) + " (file: " + field + ")");
                  }
                  if (end_date != 0 && end_date < ExtLastDate) {
                     ExtLastDate = end_date;
                  }
                  CsvClose(csvEnd);
               }
               FileDelete(randname);
               if (ExtLastDate <= 0) {
                  Print("Something went wrong, was unable to determine the last date in the file.");
               }
            }
         }
         CloseHandle(fd);
      }
   }
   return (true);
}

bool IsCorrectDelimiter(string csvFile, int delimiter) {
   int csvHandle = FileOpen(csvFile,FILE_CSV|FILE_READ,delimiter);
   string discarded = FileReadString(csvHandle, 1024);
   bool result = true;
   if (FileIsLineEnding(csvHandle)) {
      result = false;
   }
   FileClose(csvHandle);
   return (result);
}

bool HasLetters(string field) {
   bool result = false;
   for (int i = 0; i < StringLen(field); i++) {
      int chr = StringGetChar(field, i);
      if ((chr >= 65 && chr <= 90) || // A to Z
          (chr >= 97 && chr <= 122)) {// a to z
          result = true;
          break;
      }
   }
   return (result);
}

bool HasDot(string field) {
   return (StringFind(field, ".") >= 0);
}

bool HasComma(string field) {
   return (StringFind(field, ",") >= 0);
}

bool IsNumeric(string field, bool negative = false) {
   bool result = true;
   field = StringTrimRight(StringTrimLeft(field));
   for (int i = 0; i < StringLen(field); i++) {
      int chr = StringGetChar(field, i);
      if ((chr >= 48 && chr <= 57) || // 0 to 9
          chr == 46 || chr == 44 || // dot or comma
          (negative && chr == 45)) { // -
         // all good
      }
      else {
         result = false;
         break;
      }
   }
   return (result);
}

bool LooksLikeDate(string field) {
   bool result = true;
   field = StringTrimRight(StringTrimLeft(field));
   for (int i = 0; i < StringLen(field); i++) {
      int chr = StringGetChar(field, i);
      if ((chr >= 48 && chr <= 57) || // 0 to 9
          chr == 45 || chr == 47 || chr == 46 || chr == 32 || chr == 58) { // - / . [space] :
         // all good
      }
      else {
          result = false;
          break;
      }
   }
   return (result);
}

bool SkipToNextLine(int csvHandle) {
   bool result = true;
   while (!(CsvIsLineEnding(csvHandle) == 1) && !(CsvIsEnding(csvHandle) == 1)) {
      CsvReadString(csvHandle);
   }
   if (CsvIsEnding(csvHandle) == 1) {
      result = false;
   }
   return (result);
}

double SpecialStrToDouble(string field) {
   field = StringSubstr(field, 0, StringFind(field, ",")) + "." + StringSubstr(field, StringFind(field, ",") + 1);
   return (StrToDouble(field));
}

double MakeFractional(string field) {
   double value = StrToInteger(field);
   field = StringTrimLeft(StringTrimRight(field));
   for (int i = 0; i < StringLen(field); i++) {
      value /= 10;
   }
   return (value);
}

bool IsDateSeparator(int chr) {
   bool result = false;
   if (chr == 45 || chr == 47 || chr == 46 || chr == 32) { // - / . [space]
      result = true;
   }
   return (result);
}

bool ParseDate(string field, int i, datetime &d, bool check = false) {
   bool result = false;
   switch (i) {
      case 0:
         result = ParseDate0(field, d, check);
         break;
      case 1:
         result = ParseDate1(field, d, check);
         break;
      case 2:
         result = ParseDate2(field, d, check);
         break;
      case 3:
         result = ParseDate3(field, d, check);
         break;
      case 4:
         result = ParseDate4(field, d, check);
         break;
      case 5:
         result = ParseDate5(field, d, check);
         break;
      case 6:
         result = ParseDate6(field, d, check);
         break;
      case 7:
         result = ParseDate7(field, d, check);
         break;
      case 8:
         result = ParseDate8(field, d, check);
         break;
      case 9:
         result = ParseDate9(field, d, check);
         break;
      case 10:
         result = ParseDate10(field, d, check);
         break;
      case 11:
         result = ParseDate11(field, d, check);
         break;
      case 12:
         result = ParseDate12(field, d, check);
         break;
      case 13:
         result = ParseDate13(field, d, check);
         break;
      case 14:
         result = ParseDate14(field, d, check);
         break;
      case 15:
         result = ParseDate15(field, d, check);
         break;
      case 16:
         result = ParseDate16(field, d, check);
         break;
      case 17:
         result = ParseDate17(field, d, check);
         break;
      case 18:
         result = ParseDate18(field, d, check);
         break;
      case 19:
         result = ParseDate19(field, d, check);
         break;
   }
   return (result);
}

bool CheckDateCommon(string year, string month, string day, string hour, string minute, string second) {
   if (StringLen(year) == 4) {
      if (!IsNumeric(year) || StrToInteger(year) < 1970 || StrToInteger(year) > 2038) {
         return (false);
      }
   }
   else if (StringLen(year) == 2) {
      if (!IsNumeric(year) || (StrToInteger(year) > 38 && StrToInteger(year) < 70)) {
         return (false);
      }   
   }
   else {
      return (false);
   }
   if (!IsNumeric(month) || StrToInteger(month) < 1 || StrToInteger(month) > 12) {
      return (false);
   }
   if (!IsNumeric(day) || StrToInteger(day) < 1 || StrToInteger(day) > 31) {
      return (false);
   }
   if (!IsNumeric(hour) || StrToInteger(hour) < 0 || StrToInteger(hour) > 23) {
      return (false);
   }
   if (!IsNumeric(minute) || StrToInteger(minute) < 0 || StrToInteger(minute) > 60) {
      return (false);
   }
   if (!IsNumeric(second) || StrToInteger(second) < 0 || StrToInteger(second) > 60) {
      return (false);
   }
   return (true);
}

bool ParseDate0(string field, datetime &d, bool check) {
   // 20091231 12:34:56
   // 01234567890123456
   if (StringLen(field) < 17) return (false);
   string year = StringSubstr(field, 0, 4);
   string month = StringSubstr(field, 4, 2);
   string day = StringSubstr(field, 6, 2);
   string time = StringSubstr(field, 9, 8);
   if (check) {
      string hour = StringSubstr(field, 9, 2);
      string minute = StringSubstr(field, 12, 2);
      string second = StringSubstr(field, 15, 2);
      if (StringGetChar(field, 8) != 32) { // space in the middle
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
   }
   string parsabledate = year + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate1(string field, datetime &d, bool check) {
   // 20093112 12:34:56
   // 01234567890123456
   if (StringLen(field) < 17) return (false);
   string year = StringSubstr(field, 0, 4);
   string day = StringSubstr(field, 4, 2);
   string month = StringSubstr(field, 6, 2);
   string time = StringSubstr(field, 9, 8);
   if (check) {
      string hour = StringSubstr(field, 9, 2);
      string minute = StringSubstr(field, 12, 2);
      string second = StringSubstr(field, 15, 2);
      if (StringGetChar(field, 8) != 32) { // space in the middle
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
   }
   string parsabledate = year + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate2(string field, datetime &d, bool check) {
   // 31122009 12:34:56
   // 01234567890123456
   if (StringLen(field) < 17) return (false);
   string day = StringSubstr(field, 0, 2);
   string month = StringSubstr(field, 2, 2);
   string year = StringSubstr(field, 4, 4);
   string time = StringSubstr(field, 9, 8);
   if (check) {
      string hour = StringSubstr(field, 9, 2);
      string minute = StringSubstr(field, 12, 2);
      string second = StringSubstr(field, 15, 2);
      if (StringGetChar(field, 8) != 32) { // space in the middle
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
   }
   string parsabledate = year + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate3(string field, datetime &d, bool check) {
   // 12312009 12:34:56
   // 01234567890123456
   if (StringLen(field) < 17) return (false);
   string month = StringSubstr(field, 0, 2);
   string day = StringSubstr(field, 2, 2);
   string year = StringSubstr(field, 4, 4);
   string time = StringSubstr(field, 9, 8);
   if (check) {
      string hour = StringSubstr(field, 9, 2);
      string minute = StringSubstr(field, 12, 2);
      string second = StringSubstr(field, 15, 2);
      if (StringGetChar(field, 8) != 32) { // space in the middle
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
   }
   string parsabledate = year + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate4(string field, datetime &d, bool check) {
   // 123109 12:34:56
   // 012345678901234
   if (StringLen(field) < 15) return (false);
   string month = StringSubstr(field, 0, 2);
   string day = StringSubstr(field, 2, 2);
   string year = StringSubstr(field, 4, 2);
   string time = StringSubstr(field, 9, 8);
   int yearval = StrToInteger(year);
   if (yearval > 70) {
      yearval += 1900;
   }
   else {
      yearval += 2000;
   }
   if (check) {
      string hour = StringSubstr(field, 7, 2);
      string minute = StringSubstr(field, 10, 2);
      string second = StringSubstr(field, 13, 2);
      if (StringGetChar(field, 6) != 32) { // space in the middle
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
   }
   string parsabledate = (string)yearval + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate5(string field, datetime &d, bool check) {
   // 311209 12:34:56
   // 012345678901234
   if (StringLen(field) < 15) return (false);
   string day = StringSubstr(field, 0, 2);
   string month = StringSubstr(field, 2, 2);
   string year = StringSubstr(field, 4, 2);
   string time = StringSubstr(field, 9, 8);
   int yearval = StrToInteger(year);
   if (yearval > 70) {
      yearval += 1900;
   }
   else {
      yearval += 2000;
   }
   if (check) {
      string hour = StringSubstr(field, 7, 2);
      string minute = StringSubstr(field, 10, 2);
      string second = StringSubstr(field, 13, 2);
      if (StringGetChar(field, 6) != 32) { // space in the middle
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
   }
   string parsabledate = (string)yearval + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate6(string field, datetime &d, bool check) {
   // 093112 12:34:56
   // 012345678901234
   if (StringLen(field) < 15) return (false);
   string year = StringSubstr(field, 0, 2);
   string day = StringSubstr(field, 2, 2);
   string month = StringSubstr(field, 4, 2);
   string time = StringSubstr(field, 9, 8);
   int yearval = StrToInteger(year);
   if (yearval > 70) {
      yearval += 1900;
   }
   else {
      yearval += 2000;
   }
   if (check) {
      string hour = StringSubstr(field, 7, 2);
      string minute = StringSubstr(field, 10, 2);
      string second = StringSubstr(field, 13, 2);
      if (StringGetChar(field, 6) != 32) { // space in the middle
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
   }
   string parsabledate = (string)yearval + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate7(string field, datetime &d, bool check) {
   // 091231 12:34:56
   // 012345678901234
   if (StringLen(field) < 15) return (false);
   string year = StringSubstr(field, 0, 2);
   string month = StringSubstr(field, 2, 2);
   string day = StringSubstr(field, 4, 2);
   string time = StringSubstr(field, 9, 8);
   int yearval = StrToInteger(year);
   if (yearval > 70) {
      yearval += 1900;
   }
   else {
      yearval += 2000;
   }
   if (check) {
      string hour = StringSubstr(field, 7, 2);
      string minute = StringSubstr(field, 10, 2);
      string second = StringSubstr(field, 13, 2);
      if (StringGetChar(field, 6) != 32) { // space in the middle
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
   }
   string parsabledate = (string)yearval + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate8(string field, datetime &d, bool check) {
   // 2009?12?31 12:34:56
   // 0123456789012345678
   if (StringLen(field) < 19) return (false);
   string year = StringSubstr(field, 0, 4);
   string month = StringSubstr(field, 5, 2);
   string day = StringSubstr(field, 8, 2);
   string time = StringSubstr(field, 11, 8);
   if (check) {
      string hour = StringSubstr(field, 11, 2);
      string minute = StringSubstr(field, 14, 2);
      string second = StringSubstr(field, 17, 2);
      if (StringGetChar(field, 10) != 32) { // space in the middle
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 4))) { // separator 1
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 7))) { // separator 2
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
      ExtDateSeparator = StringGetChar(field, 4);
   }
   string parsabledate = year + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate9(string field, datetime &d, bool check) {
   // 2009?31?12 12:34:56
   // 0123456789012345678
   if (StringLen(field) < 19) return (false);
   string year = StringSubstr(field, 0, 4);
   string day = StringSubstr(field, 5, 2);
   string month = StringSubstr(field, 8, 2);
   string time = StringSubstr(field, 11, 8);
   if (check) {
      string hour = StringSubstr(field, 11, 2);
      string minute = StringSubstr(field, 14, 2);
      string second = StringSubstr(field, 17, 2);
      if (StringGetChar(field, 10) != 32) { // space in the middle
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 4))) { // separator 1
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 7))) { // separator 2
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
      ExtDateSeparator = StringGetChar(field, 4);
   }
   string parsabledate = year + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate10(string field, datetime &d, bool check) {
   // 31?12?2009 12:34:56
   // 0123456789012345678
   if (StringLen(field) < 19) return (false);
   string day = StringSubstr(field, 0, 2);
   string month = StringSubstr(field, 3, 2);
   string year = StringSubstr(field, 6, 4);
   string time = StringSubstr(field, 11, 8);
   if (check) {
      string hour = StringSubstr(field, 11, 2);
      string minute = StringSubstr(field, 14, 2);
      string second = StringSubstr(field, 17, 2);
      if (StringGetChar(field, 10) != 32) { // space in the middle
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 2))) { // separator 1
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 5))) { // separator 2
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
      ExtDateSeparator = StringGetChar(field, 2);
   }
   string parsabledate = year + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate11(string field, datetime &d, bool check) {
   // 12?31?2009 12:34:56
   // 0123456789012345678
   if (StringLen(field) < 19) return (false);
   string month = StringSubstr(field, 0, 2);
   string day = StringSubstr(field, 3, 2);
   string year = StringSubstr(field, 6, 4);
   string time = StringSubstr(field, 11, 8);
   if (check) {
      string hour = StringSubstr(field, 11, 2);
      string minute = StringSubstr(field, 14, 2);
      string second = StringSubstr(field, 17, 2);
      if (StringGetChar(field, 10) != 32) { // space in the middle
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 2))) { // separator 1
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 5))) { // separator 2
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
      ExtDateSeparator = StringGetChar(field, 2);
   }
   string parsabledate = year + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate12(string field, datetime &d, bool check) {
   // 12?31?09 12:34:56
   // 01234567890123456
   if (StringLen(field) < 17) return (false);
   string month = StringSubstr(field, 0, 2);
   string day = StringSubstr(field, 3, 2);
   string year = StringSubstr(field, 6, 2);
   string time = StringSubstr(field, 9, 8);
   int yearval = StrToInteger(year);
   if (yearval > 70) {
      yearval += 1900;
   }
   else {
      yearval += 2000;
   }
   if (check) {
      string hour = StringSubstr(field, 9, 2);
      string minute = StringSubstr(field, 12, 2);
      string second = StringSubstr(field, 15, 2);
      if (StringGetChar(field, 8) != 32) { // space in the middle
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 2))) { // separator 1
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 5))) { // separator 2
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
      ExtDateSeparator = StringGetChar(field, 2);
   }
   string parsabledate = (string)yearval + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate13(string field, datetime &d, bool check) {
   // 31?12?09 12:34:56
   // 01234567890123456
   if (StringLen(field) < 17) return (false);
   string day = StringSubstr(field, 0, 2);
   string month = StringSubstr(field, 3, 2);
   string year = StringSubstr(field, 6, 2);
   string time = StringSubstr(field, 9, 8);
   int yearval = StrToInteger(year);
   if (yearval > 70) {
      yearval += 1900;
   }
   else {
      yearval += 2000;
   }
   if (check) {
      string hour = StringSubstr(field, 9, 2);
      string minute = StringSubstr(field, 12, 2);
      string second = StringSubstr(field, 15, 2);
      if (StringGetChar(field, 8) != 32) { // space in the middle
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 2))) { // separator 1
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 5))) { // separator 2
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
      ExtDateSeparator = StringGetChar(field, 2);
   }
   string parsabledate = (string)yearval + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate14(string field, datetime &d, bool check) {
   // 09?12?31 12:34:56
   // 01234567890123456
   if (StringLen(field) < 17) return (false);
   string year = StringSubstr(field, 0, 2);
   string month = StringSubstr(field, 3, 2);
   string day = StringSubstr(field, 6, 2);
   string time = StringSubstr(field, 9, 8);
   int yearval = StrToInteger(year);
   if (yearval > 70) {
      yearval += 1900;
   }
   else {
      yearval += 2000;
   }
   if (check) {
      string hour = StringSubstr(field, 9, 2);
      string minute = StringSubstr(field, 12, 2);
      string second = StringSubstr(field, 15, 2);
      if (StringGetChar(field, 8) != 32) { // space in the middle
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 2))) { // separator 1
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 5))) { // separator 2
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
      ExtDateSeparator = StringGetChar(field, 2);
   }
   string parsabledate = (string)yearval + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate15(string field, datetime &d, bool check) {
   // 09?31?12 12:34:56
   // 01234567890123456
   if (StringLen(field) < 17) return (false);
   string year = StringSubstr(field, 0, 2);
   string day = StringSubstr(field, 3, 2);
   string month = StringSubstr(field, 6, 2);
   string time = StringSubstr(field, 9, 8);
   int yearval = StrToInteger(year);
   if (yearval > 70) {
      yearval += 1900;
   }
   else {
      yearval += 2000;
   }
   if (check) {
      string hour = StringSubstr(field, 9, 2);
      string minute = StringSubstr(field, 12, 2);
      string second = StringSubstr(field, 15, 2);
      if (StringGetChar(field, 8) != 32) { // space in the middle
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 2))) { // separator 1
         return (false);
      }
      if (!IsDateSeparator(StringGetChar(field, 5))) { // separator 2
         return (false);
      }
      if (!IsNumeric(year) || (StrToInteger(year) > 38 && StrToInteger(year) < 70)) {
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
      ExtDateSeparator = StringGetChar(field, 2);
   }
   string parsabledate = (string)yearval + "." + month + "." + day + " " + time;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate16(string field, datetime &d, bool check) {
   // 20121231 123456???
   // 01234567890123456
   if (StringLen(field) < 15) return (false);
   string year = StringSubstr(field, 0, 4);
   string month = StringSubstr(field, 4, 2);
   string day = StringSubstr(field, 6, 2);
   string hour = StringSubstr(field, 9, 2);
   string minute = StringSubstr(field, 11, 2);
   string second = StringSubstr(field, 13, 2);
   int yearval = StrToInteger(year);
   if (check) {
      if (StringGetChar(field, 8) != 32) { // space in the middle
         return (false);
      }
      if (!IsNumeric(year) || (StrToInteger(year) > 38 && StrToInteger(year) < 70)) {
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
      ExtDateSeparator = 0;
   }
   string parsabledate = (string)yearval + "." + month + "." + day + " " + (string)hour + ":" + (string)minute + ":" + (string)second;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate17(string field, datetime &d, bool check) {
   // 20123112 123456???
   // 01234567890123456
   if (StringLen(field) < 15) return (false);
   string year = StringSubstr(field, 0, 4);
   string day = StringSubstr(field, 4, 2);
   string month = StringSubstr(field, 6, 2);
   string hour = StringSubstr(field, 9, 2);
   string minute = StringSubstr(field, 11, 2);
   string second = StringSubstr(field, 13, 2);
   int yearval = StrToInteger(year);
   if (check) {
      if (StringGetChar(field, 8) != 32) { // space in the middle
         return (false);
      }
      if (!IsNumeric(year) || (StrToInteger(year) > 38 && StrToInteger(year) < 70)) {
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
      ExtDateSeparator = 0;
   }
   string parsabledate = (string)yearval + "." + month + "." + day + " " + hour + ":" + minute + ":" + second;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate18(string field, datetime &d, bool check) {
   // 31122012 123456???
   // 01234567890123456
   if (StringLen(field) < 15) return (false);
   string day = StringSubstr(field, 0, 2);
   string month = StringSubstr(field, 2, 2);
   string year = StringSubstr(field, 4, 4);
   string hour = StringSubstr(field, 9, 2);
   string minute = StringSubstr(field, 11, 2);
   string second = StringSubstr(field, 13, 2);
   int yearval = StrToInteger(year);
   if (check) {
      if (StringGetChar(field, 8) != 32) { // space in the middle
         return (false);
      }
      if (!IsNumeric(year) || (StrToInteger(year) > 38 && StrToInteger(year) < 70)) {
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
      ExtDateSeparator = 0;
   }
   string parsabledate = (string)yearval + "." + month + "." + day + " " + hour + ":" + minute + ":" + second;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

bool ParseDate19(string field, datetime &d, bool check) {
   // 12312012 123456???
   // 01234567890123456
   if (StringLen(field) < 15) return (false);
   string month = StringSubstr(field, 0, 2);
   string day = StringSubstr(field, 2, 2);
   string year = StringSubstr(field, 4, 4);
   string hour = StringSubstr(field, 9, 2);
   string minute = StringSubstr(field, 11, 2);
   string second = StringSubstr(field, 13, 2);
   int yearval = StrToInteger(year);
   if (check) {
      if (StringGetChar(field, 8) != 32) { // space in the middle
         return (false);
      }
      if (!IsNumeric(year) || (StrToInteger(year) > 38 && StrToInteger(year) < 70)) {
         return (false);
      }
      if (!CheckDateCommon(year, month, day, hour, minute, second)) {
         return (false);
      }
      ExtDateSeparator = 0;
   }
   string parsabledate = (string)yearval + "." + month + "." + day + " " + hour + ":" + minute + ":" + second;
   d = StrToTime(parsabledate);
   return (d >= 0);
}

string DateFormatToStr(int i) {
   string result = "unknown";
   string separator = "";
   if (ExtDateSeparator > 0) {
      separator = StringSetChar(separator, 0, (ushort)ExtDateSeparator);
   }
   switch (i) {
      case 0:
         result = "YYYYMMDD hh:mm:ss";
         break;
      case 1:
         result = "YYYYDDMM hh:mm:ss";
         break;
      case 2:
         result = "DDMMYYYY hh:mm:ss";
         break;
      case 3:
         result = "MMDDYYYY hh:mm:ss";
         break;
      case 4:
         result = "MMDDYY hh:mm:ss";
         break;
      case 5:
         result = "DDMMYY hh:mm:ss";
         break;
      case 6:
         result = "YYDDMM hh:mm:ss";
         break;
      case 7:
         result = "YYMMDD hh:mm:ss";
         break;
      case 8:
         result = "YYYY" + separator + "MM" + separator + "DD hh:mm:ss";
         break;
      case 9:
         result = "YYYY" + separator + "DD" + separator + "MM hh:mm:ss";
         break;
      case 10:
         result = "DD" + separator + "?MM" + separator + "YYYY hh:mm:ss";
         break;
      case 11:
         result = "MM" + separator + "DD" + separator + "YYYY hh:mm:ss";
         break;
      case 12:
         result = "MM" + separator + "DD" + separator + "YY hh:mm:ss";
         break;
      case 13:
         result = "DD" + separator + "MM" + separator + "YY hh:mm:ss";
         break;
      case 14:
         result = "YY" + separator + "MM" + separator + "DD hh:mm:ss";
         break;
      case 15:
         result = "YY" + separator + "DD" + separator + "MM hh:mm:ss";
         break;
      case 16:
         result = "YYYYMMDD hhmmss";
         break;
      case 17:
         result = "YYYYDDMM hhmmss";
         break;
      case 18:
         result = "DDMMYYYY hhmmss";
         break;
      case 19:
         result = "MMDDYYYY hhmmss";
         break;
   }
   return (result);
}

bool HasExtraDigit() {
// add code here if you're backtesting a symbol with strange particularities, such as a misc CFD or e.g. XAGJPY
   if (Digits % 2 == 1) {
      return (true);
   }
   return (false);
}

string DllVersion(string dllName) {
   //-- Fetch the DLL version number
   int    i, vSize, aSize, vInfo[];
   string tPath, vChar, vString;

   tPath = ExtTerminalPath + "\\MQL4\\Libraries\\" + dllName;
   vSize = GetFileVersionInfoSizeW(tPath, 0);
   aSize = (vSize + 3) / 4;
   ArrayResize(vInfo, aSize);
   if (GetFileVersionInfoW(tPath, 0, vSize, vInfo) == 0) {
      return "";
   }
   for(i = 0; i < aSize; i++){
      if (vInfo[i] == 0) continue;
      int val = vInfo[i] & 0x0000FFFF;
      vChar = CharToStr((char)(vInfo[i] & 0x000000FF));
      if (vChar == "") vChar = " ";
      vString += vChar;
      vChar = CharToStr((char)((vInfo[i] >> 16) & 0x000000FF));
      if (vChar == "") vChar = " ";
      vString += vChar;
   }
   return (StringTrimRight(StringTrimLeft(StringSubstr(vString, StringFind(vString, "FileVersion") + 11, 10))));
} 