package bi5

import (
    "fmt"
    "testing"
    "time"
)

func TestLoadBi5(t *testing.T) {
    //fname := `F:\00\EURUSD\2017\01\01\22h.bi5`
    dest := `F:\00`

    day, err := time.ParseInLocation("2006-01-02 15", "2017-01-01 22", time.UTC)
    if err != nil {
        t.Fatalf("Invalid date format\n")
    }

    fb := New(day, "EURUSD", dest)
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
}

func TestDownloadBi5(t *testing.T) {
    //fname := `F:\00\EURUSD\2017\01\01\22h.bi5`
    dest := `F:\test01`

    day, err := time.ParseInLocation("2006-01-02 15", "2017-01-01 22", time.UTC)
    if err != nil {
        t.Fatalf("Invalid date format\n")
    }

    fb := New(day, "EURUSD", dest)
    bs, err := fb.Download()
    if err != nil {
        t.Fatalf("Load bi5 failed: %v.\n", err)
    }

    defer fb.Save(bs[:])

    ticks, err := fb.Decode(bs[:])
    if err != nil {
        t.Fatalf("Decode bi5 failed: %v.\n", err)
    }

    for idx, tick := range ticks {
        fmt.Printf("%d:  %v\n", idx, tick)
    }

}
