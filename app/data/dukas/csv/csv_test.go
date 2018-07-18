package csv

import (
    "fmt"
    "testing"
    "time"

    "github.com/adyzng/go-duka/bi5"
)

func TestCloseChan(t *testing.T) {
    chClose := make(chan struct{}, 1)
    go func() {
        defer close(chClose)
        time.Sleep(2 * time.Second)
        t.Logf("Close chan.\n")
    }()

    <-chClose
    t.Logf("Receive close channel.\n")
}

func TestDumpCsv(t *testing.T) {
    dest := `F:\00`
    symbol := "EURUSD"

    day, err := time.ParseInLocation("2006-01-02", "2017-01-02", time.UTC)
    if err != nil {
        t.Fatalf("Invalid date format\n")
    }

    csv := New(day, day, true, symbol, dest)
    defer csv.Finish()

    for h := 0; h < 24; h++ {
        dayH := day.Add(time.Duration(h) * time.Hour)
        fb := bi5.New(dayH, symbol, dest)

        bs, err := fb.Load()
        if err != nil {
            t.Fatalf("Load bi5 failed: %v.\n", err)
        }

        ticks, err := fb.Decode(bs[:])
        if err != nil {
            t.Fatalf("Decode bi5 failed: %v.\n", err)
        }

        for idx, tick := range ticks {
            fmt.Printf("%d:  %v\n", idx, tick)
        }

        csv.PackTicks(0, ticks)
    }
}
