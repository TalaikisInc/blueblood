package core

import (
    "regexp"
    "strconv"
)

var (
    TimeframeRegx = regexp.MustCompile(`(M|H|D|W|MN)(\d+)`)
    tfMinute      = map[string]uint32{
        "M":  1,
        "H":  60,
        "D":  24 * 60,
        "W":  7 * 24 * 60,
        "MN": 30 * 24 * 60,
    }
)

// Timeframe wrapper of tick data in timeframe like: M1, M5, M15, M30, H1, H4, D1, W1, MN
//
type Timeframe struct {
    deltaTimestamp uint32 // unit second
    startTimestamp uint32 // unit second
    endTimestamp   uint32 // unit second
    timeframe      uint32 // Period of data aggregation in minutes
    period         string // M1, M5, M15, M30, H1, H4, D1, W1, MN
    symbol         string

    chTicks chan *TickData
    close   chan struct{}
    out     Converter
}

// ParseTimeframe from input string
//
func ParseTimeframe(period string) (uint32, string) {
    // M15 => [M15 M 15]
    if ss := TimeframeRegx.FindStringSubmatch(period); len(ss) == 3 {
        n, _ := strconv.Atoi(ss[2])
        for key, val := range tfMinute {
            if key == ss[1] {
                return val * uint32(n), ss[0]
            }
        }
    }
    return 1, "M1" // M1 by default
}

// NewTimeframe create an new timeframe
func NewTimeframe(period, symbol string, out Converter) Converter {
    min, str := ParseTimeframe(period)
    tf := &Timeframe{
        deltaTimestamp: min * 60,
        timeframe:      min,
        period:         str,
        symbol:         symbol,
        out:            out,
        chTicks:        make(chan *TickData, 1024),
        close:          make(chan struct{}, 1),
    }

    go tf.worker()
    return tf
}

// PackTicks receive original tick data
func (tf *Timeframe) PackTicks(barTimestamp uint32, ticks []*TickData) error {
    for _, tick := range ticks {
        select {
        case tf.chTicks <- tick:
            break
        }
    }
    return nil
}

// Finish wait convert finish
func (tf *Timeframe) Finish() error {
    close(tf.chTicks)
    <-tf.close
    return tf.out.Finish()
}

// worker thread
func (tf *Timeframe) worker() error {
    maxCap := 1024
    barTicks := make([]*TickData, 0, maxCap)

    defer func() {
        log.Info("%s %s convert completed.", tf.symbol, tf.period)
        close(tf.close)
    }()

    var tickSeconds uint32
    var tickBarTime uint32

    for tick := range tf.chTicks {
        // Beginning of the bar's timeline.
        tickSeconds = uint32(tick.Timestamp / 1000)
        tickBarTime = tickSeconds - tickSeconds%tf.deltaTimestamp

        if tf.startTimestamp == 0 {
            tf.startTimestamp = tickBarTime
            tf.endTimestamp = tickBarTime + tf.deltaTimestamp
        }

        //Determines the end of the current bar.
        if tickSeconds >= tf.endTimestamp {
            // output one bar data
            if len(barTicks) > 0 {
                tf.out.PackTicks(tf.startTimestamp, barTicks[:])
                barTicks = barTicks[:0]
            }

            // Next bar's timeline will begin from this new tick's bar
            tf.startTimestamp = tickBarTime
            tf.endTimestamp = tf.startTimestamp + tf.deltaTimestamp

            // start next round bar
            barTicks = append(barTicks, tick)

        } else {
            // Tick is within the current bar's timeline, queue it
            barTicks = append(barTicks, tick)
        }
    }

    if len(barTicks) > 0 {
        tf.out.PackTicks(tf.startTimestamp, barTicks[:])
    }

    return nil
}
