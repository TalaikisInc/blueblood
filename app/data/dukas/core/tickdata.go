package core

import (
    "fmt"
    "time"
)

// TickData for dukascopy
//
type TickData struct {
    Symbol    string  // 货币对
    Timestamp int64   // 时间戳(ms)
    Ask       float64 // 卖价
    Bid       float64 // 买价
    VolumeAsk float64 // 单位：通常是按10万美元为一手，最小0.01手
    VolumeBid float64 // 单位：...
}

// UTC convert timestamp to UTC time
//
func (t *TickData) UTC() time.Time {
    tm := time.Unix(t.Timestamp/1000, (t.Timestamp%1000)*int64(time.Millisecond))
    return tm.UTC()
}

// Strings used to format into csv row
//
func (t *TickData) Strings() []string {
    return []string{
        t.UTC().Format("2006-01-02 15:04:05.000"),
        fmt.Sprintf("%.5f", t.Ask),
        fmt.Sprintf("%.5f", t.Bid),
        fmt.Sprintf("%.2f", t.VolumeAsk),
        fmt.Sprintf("%.2f", t.VolumeBid),
    }
}

func (t *TickData) String() string {
    return fmt.Sprintf("%s %.5f %.5f %.2f %.2f",
        t.UTC().Format("2006-01-02 15:04:06.000"),
        t.Ask,
        t.Bid,
        t.VolumeAsk,
        t.VolumeBid,
    )
}
