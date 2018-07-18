package main

import (
    "fmt"
    "testing"

    clog "github.com/go-clog/clog"
)

func TestDukaApp(t *testing.T) {
    args := argsList{
        Verbose: true,
        Header:  true,
        Spread:  20,
        Model:   0,
        Symbol:  "EURUSD",
        Output:  "f:\\00",
        Format:  "csv",
        Period:  "M1",
        Start:   "2017-01-01",
        End:     "2017-01-03",
    }

    opt, err := ParseOption(args)
    if err != nil {
        fmt.Println(err)
        return
    }

    fmt.Printf("    Output: %s\n", opt.Folder)
    fmt.Printf("    Symbol: %s\n", opt.Symbol)
    fmt.Printf("    Spread: %d\n", opt.Spread)
    fmt.Printf("      Mode: %d\n", opt.Mode)
    fmt.Printf(" Timeframe: %d\n", opt.Timeframe)
    fmt.Printf("    Format: %s\n", opt.Format)
    fmt.Printf(" CsvHeader: %t\n", opt.CsvHeader)
    fmt.Printf(" StartDate: %s\n", opt.Start.Format("2006-01-02:15H"))
    fmt.Printf("   EndDate: %s\n", opt.End.Format("2006-01-02:15H"))

    defer clog.Shutdown()
    app := NewApp(opt)
    app.Execute()
}
