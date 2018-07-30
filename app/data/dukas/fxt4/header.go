package fxt4

import (
    "fmt"
    "time"

    "github.com/adyzng/go-duka/misc"
)

var (
    headerSize = 728
    tickSize   = 56
)

// FXTHeader History Files in FXT Format
// https://www.metatrader4.com/en/trading-platform/help/autotrading/tester/tester_fxt
//
// Documentation on the format can be found in terminal Help (Client terminal - Auto Trading - Strategy Testing - History Files FXT).
// However the obtained data shows that the data does not match the declared format.
// In the eye catches the fact that the work is carried out over time in both formats: the new and the old MQL4.
// So, members of fromdate and todate structure TestHistoryHeader , and ctm structure TestHistory use the old (4 hbaytny) date / time format, but a member of otm structure TestHistory written in the new (8-byte) date / time format.
// It is unclear whether the correct type of selected members unknown.
// The FXT as teak prices recorded only Bid, but its spread is written in the Volume field.
// By breaking MT4 is obtained to ensure that the MT4-tester figured on each tick Ask, how the Bid + the Volume (that's the trick).
// Source: https://forum.mql4.com/ru/64199/page3
type FXTHeader struct {
    //Header layout--------------------- offset --- size --- description ------------------------------------------------------------------------
    Version      uint32    //                    0        4     header version:
    Description  [64]byte  //                    4       64     copyright/description (szchar)
    ServerName   [128]byte //                   68      128     account server name (szchar)
    Symbol       [12]byte  //                  196       12     symbol (szchar)
    Period       uint32    //                  208        4     timeframe in minutes
    ModelType    uint32    //                  212        4     0=EveryTick|1=ControlPoints|2=BarOpen
    ModeledBars  uint32    //                  216        4     number of modeled bars      (w/o prolog)
    FirstBarTime uint32    //                  220        4     bar open time of first tick (w/o prolog)
    LastBarTime  uint32    //                  224        4     bar open time of last tick  (w/o prolog)
    _            [4]byte   //                  228        4     (alignment to the next double)
    ModelQuality float64   //                  232        8     max. 99.9

    // common parameters-----------------------------------------------------------------------------------------------------------------------
    BaseCurrency [12]byte //                 240       12     base currency (szchar)                     = StringLeft(symbol, 3)
    Spread       uint32   //                 252        4     spread in points: 0=zero spread            = MarketInfo(MODE_SPREAD)
    Digits       uint32   //                 256        4     digits                                     = MarketInfo(MODE_DIGITS)
    _            [4]byte  //                 260        4     (alignment to the next double)
    PointSize    float64  //                 264        8     resolution, ie. 0.0000'1                   = MarketInfo(MODE_POINT)
    MinLotsize   uint32   //                 272        4     min lot size in centi lots (hundredths)    = MarketInfo(MODE_MINLOT)  * 100
    MaxLotsize   uint32   //                 276        4     max lot size in centi lots (hundredths)    = MarketInfo(MODE_MAXLOT)  * 100
    LotStepsize  uint32   //                 280        4     lot stepsize in centi lots (hundredths)    = MarketInfo(MODE_LOTSTEP) * 100
    StopsLevel   uint32   //                 284        4     orders stop distance in points             = MarketInfo(MODE_STOPLEVEL)
    PendingsGTC  uint32   //                 288        4     close pending orders at end of day or GTC
    _            [4]byte  //                 292        4     (alignment to the next double)

    // profit calculation parameters-------------------------------------------------------------------------------------------------------------
    ContractSize          float64 //          296        8     ie. 100000                                 = MarketInfo(MODE_LOTSIZE)
    TickValue             float64 //          304        8     tick value in quote currency (empty)       = MarketInfo(MODE_TICKVALUE)
    TickSize              float64 //          312        8     tick size (empty)                          = MarketInfo(MODE_TICKSIZE)
    ProfitCalculationMode uint32  //          320        4     0=Forex|1=CFD|2=Futures                    = MarketInfo(MODE_PROFITCALCMODE)

    // swap calculation parameters -------------------------------------------------------------------------------------------------------------
    SwapEnabled         uint32  //          324        4     if swaps are to be applied
    SwapCalculationMode int32   //          328        4     0=Points|1=BaseCurrency|2=Interest|3=MarginCurrency   = MarketInfo(MODE_SWAPTYPE)
    _                   [4]byte //          332        4     (alignment to the next double)
    SwapLongValue       float64 //          336        8     long overnight swap value                  = MarketInfo(MODE_SWAPLONG)
    SwapShortValue      float64 //          344        8     short overnight swap values                = MarketInfo(MODE_SWAPSHORT)
    TripleRolloverDay   uint32  //          352        4     weekday of triple swaps                    = WEDNESDAY (3)

    // margin calculation parameters -------------------------------------------------------------------------------------------------------------
    AccountLeverage           uint32   //     356        4     account leverage                           = AccountLeverage()
    FreeMarginCalculationType uint32   //     360        4     free margin calculation type               = AccountFreeMarginMode()
    MarginCalculationMode     uint32   //     364        4     margin calculation mode                    = MarketInfo(MODE_MARGINCALCMODE)
    MarginStopoutLevel        uint32   //     368        4     margin stopout level                       = AccountStopoutLevel()
    MarginStopoutType         uint32   //     372        4     margin stopout type                        = AccountStopoutMode()
    MarginInit                float64  //     376        8     initial margin requirement (in units)      = MarketInfo(MODE_MARGININIT)
    MarginMaintenance         float64  //     384        8     maintainance margin requirement (in units) = MarketInfo(MODE_MARGINMAINTENANCE)
    MarginHedged              float64  //     392        8     hedged margin requirement (in units)       = MarketInfo(MODE_MARGINHEDGED)
    MarginDivider             float64  //     400        8     leverage calculation                         @see example in struct SYMBOL
    MarginCurrency            [12]byte //     408       12                                                = AccountCurrency()
    _                         [4]byte  //     420        4     (alignment to the next double)

    // commission calculation parameters ----------------------------------------------------------------------------------------------------------
    CommissionValue           float64 //     424        8     commission rate
    CommissionCalculationMode int32   //     432        4     0=Money|1=Pips|2=Percent                     @see COMMISSION_MODE_*
    CommissionType            int32   //     436        4     0=RoundTurn|1=PerDeal                        @see COMMISSION_TYPE_*

    // later additions-----------------------------------------------------------------------------------------------------------------------------
    FirstBar          uint32    //          440        4     bar number/index??? of first bar (w/o prolog) or 0 for first bar
    LastBar           uint32    //          444        4     bar number/index??? of last bar (w/o prolog) or 0 for last bar
    StartPeriodM1     uint32    //          448        4     bar index where modeling started using M1 bars
    StartPeriodM5     uint32    //          452        4     bar index where modeling started using M5 bars
    StartPeriodM15    uint32    //          456        4     bar index where modeling started using M15 bars
    StartPeriodM30    uint32    //          460        4     bar index where modeling started using M30 bars
    StartPeriodH1     uint32    //          464        4     bar index where modeling started using H1 bars
    StartPeriodH4     uint32    //          468        4     bar index where modeling started using H4 bars
    TesterSettingFrom uint32    //          472        4     begin date from tester settings
    TesterSettingTo   uint32    //          476        4     end date from tester settings
    FreezeDistance    uint32    //          480        4     order freeze level in points               = MarketInfo(MODE_FREEZELEVEL)
    ModelErrors       uint32    //          484        4     number of errors during model generation (FIX ERRORS SHOWING UP HERE BEFORE TESTING
    _                 [240]byte //          488      240     unused
}

// FxtTick ...
//
type FxtTick struct {
    BarTimestamp  uint64  //   0  8   Bar datetime, align with timeframe, unit seconds
    Open          float64 //   8  8
    High          float64 //  16  8
    Low           float64 //  24  8
    Close         float64 //  32  8
    Volume        uint64  //  40  8   Volume (documentation says it's a double, though it's stored as a long int)
    TickTimestamp uint32  //  48  4   tick data timestamp in seconds
    LaunchExpert  uint32  //  52  4   Flag to launch an expert (0 - bar will be modified, but the expert will not be launched).
}

// NewHeader return an predefined FXT header
func NewHeader(version uint32, symbol string, timeframe, spread, model uint32) *FXTHeader {
    h := &FXTHeader{
        Version:      version,
        Period:       timeframe,
        ModelType:    model,
        ModelQuality: 99.9,

        // General parameters.
        Spread:      spread,
        Digits:      5,
        PointSize:   1e-5,
        MinLotsize:  1,
        MaxLotsize:  50000,
        LotStepsize: 1,
        StopsLevel:  10,
        PendingsGTC: 1,

        // Profit Calculation parameters.
        ContractSize:          100000,
        TickValue:             0,
        TickSize:              0,
        ProfitCalculationMode: 0,

        // Swap calculation
        SwapEnabled:         0,
        SwapCalculationMode: 0,
        SwapLongValue:       0,
        SwapShortValue:      0,
        TripleRolloverDay:   3,

        // Margin calculation.
        AccountLeverage:           100,
        FreeMarginCalculationType: 1,
        MarginCalculationMode:     0,
        MarginStopoutLevel:        30,
        MarginStopoutType:         0,
        MarginInit:                0.0,
        MarginMaintenance:         0.0,
        MarginHedged:              50000.0,
        MarginDivider:             1.25,

        // Commission calculation
        CommissionValue:           0.0,
        CommissionCalculationMode: 1,
        CommissionType:            0,

        //  For internal use
        FirstBar: 1,
    }

    misc.ToFixBytes(h.Description[:], "Copyright 2001-2017, MetaQuotes Software Corp.")
    misc.ToFixBytes(h.ServerName[:], "Beijing MoreU Tech.")
    misc.ToFixBytes(h.Symbol[:], symbol)
    misc.ToFixBytes(h.BaseCurrency[:], symbol[:3])
    misc.ToFixBytes(h.MarginCurrency[:], symbol[:3])

    return h
}

func (h *FXTHeader) ToBytes() ([]byte, error) {
    bs, err := misc.PackLittleEndian(headerSize, h)
    if err != nil {
        log.Error("Failed to convert FXT header to bytes array. Error %v.", err)
        return make([]byte, 0), err
    }
    return bs, err
}

func (t *FxtTick) ToBytes() ([]byte, error) {
    bs, err := misc.PackLittleEndian(tickSize, t)
    if err != nil {
        log.Error("Failed to convert FXT tick to bytes array. Error %v.", err)
        return make([]byte, 0), err
    }
    return bs, err
}

func (t *FxtTick) String() string {
    bt := time.Unix(int64(t.BarTimestamp), 0).UTC()
    tt := time.Unix(int64(t.TickTimestamp), 0).UTC()
    return fmt.Sprintf("%s %s %f %f %f %f %v",
        Format("2006-01-02 15:04:05"),
        tt.Format("2006-01-02 15:04:05"),
        t.Open,
        t.High,
        t.Low,
        t.Close,
        t.Volume,
    )
}
