package csv

import (
    "encoding/csv"
    "fmt"
    "os"
    "path/filepath"
    "time"

    "github.com/adyzng/go-duka/core"
    "github.com/adyzng/go-duka/misc"
)

var (
    ext       = "CSV"
    log       = misc.NewLogger("CSV", 3)
    csvHeader = []string{"time", "ask", "bid", "ask_volume", "bid_volume"}
)

// CsvDump save csv format
type CsvDump struct {
    day       time.Time
    end       time.Time
    dest      string
    symbol    string
    header    bool
    tickCount int64
    chClose   chan struct{}
    chTicks   chan *core.TickData
}

// New Csv file
func New(start, end time.Time, header bool, symbol, dest string) *CsvDump {
    csv := &CsvDump{
        day:     start,
        end:     end,
        dest:    dest,
        symbol:  symbol,
        header:  header,
        chClose: make(chan struct{}, 1),
        chTicks: make(chan *core.TickData, 1024),
    }

    go csv.worker()
    return csv
}

// Finish complete csv file writing
//
func (c *CsvDump) Finish() error {
    close(c.chTicks)
    <-c.chClose
    return nil
}

// PackTicks handle ticks data
//
func (c *CsvDump) PackTicks(barTimestamp uint32, ticks []*core.TickData) error {
    for _, tick := range ticks {
        select {
        case c.chTicks <- tick:
            c.tickCount++
            break
        }
    }
    return nil
}

// worker goroutine which flust data to disk
//
func (c *CsvDump) worker() error {
    fname := fmt.Sprintf("%s-%s-%s.%s",
        c.symbol,
        c.day.Format("2006-01-02"),
        c.end.Format("2006-01-02"),
        ext)

    fpath := filepath.Join(c.dest, fname)
    f, err := os.OpenFile(fpath, os.O_CREATE|os.O_TRUNC|os.O_RDWR, 666)
    if err != nil {
        log.Error("Failed to create file %s, error %v.", fpath, err)
        return err
    }

    defer func() {
        f.Close()
        close(c.chClose)
        log.Info("Saved Ticks: %d.", c.tickCount)
    }()

    csv := csv.NewWriter(f)
    defer csv.Flush()

    // write header
    if c.header {
        csv.Write(csvHeader)
    }

    // write tick one by one
    for tick := range c.chTicks {
        if err = csv.Write(tick.Strings()); err != nil {
            log.Error("Write csv %s failed: %v.", fpath, err)
            break
        }
    }

    return err
}
