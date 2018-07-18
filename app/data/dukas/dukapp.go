package main

import (
    "errors"
    "fmt"
    "os"
    "path/filepath"
    "sort"
    "strings"
    "sync"
    "time"

    "github.com/adyzng/go-duka/bi5"
    "github.com/adyzng/go-duka/core"
    "github.com/adyzng/go-duka/csv"
    "github.com/adyzng/go-duka/fxt4"
    "github.com/adyzng/go-duka/hst"
    "github.com/adyzng/go-duka/misc"
)

var (
    log             = misc.NewLogger("App", 2)
    supportsFormats = []string{"csv", "fxt", "hst"}
)

// DukaApp used to download source tick data
//
type DukaApp struct {
    option  AppOption
    outputs []core.Converter
}

// AppOption download options
//
type AppOption struct {
    Start     time.Time
    End       time.Time
    Symbol    string
    Format    string
    Folder    string
    Periods   string
    Spread    uint32
    Mode      uint32
    Local     bool
    CsvHeader bool
}

// ParseOption parse input command line
//
func ParseOption(args argsList) (*AppOption, error) {
    var err error
    opt := AppOption{
        CsvHeader: args.Header,
        Local:     args.Local,
        Format:    args.Format,
        Symbol:    strings.ToUpper(args.Symbol),
        Spread:    uint32(args.Spread),
        Mode:      uint32(args.Model),
    }

    if args.Symbol == "" {
        err = fmt.Errorf("Invalid symbol parameter")
        return nil, err
    }
    // check format
    {
        bSupport, format := false, strings.ToLower(args.Format)
        for _, sformat := range supportsFormats {
            if format == sformat {
                bSupport = true
                break
            }
        }
        if !bSupport {
            err = fmt.Errorf("not supported output format")
            return nil, err
        }
        opt.Format = format
    }
    if opt.Start, err = time.ParseInLocation("2006-01-02", args.Start, time.UTC); err != nil {
        err = fmt.Errorf("invalid start parameter")
        return nil, err
    }
    if opt.End, err = time.ParseInLocation("2006-01-02", args.End, time.UTC); err != nil {
        err = fmt.Errorf("invalid end parameter")
        return nil, nil
    }
    if opt.End.Unix() <= opt.Start.Unix() {
        err = fmt.Errorf("invalid end parameter which shouldn't early then start")
        return nil, err
    }
    if opt.Folder, err = filepath.Abs(args.Output); err != nil {
        err = fmt.Errorf("invalid destination folder")
        return nil, err
    }
    if err = os.MkdirAll(opt.Folder, 666); err != nil {
        err = fmt.Errorf("create destination folder failed: %v", err)
        return nil, err
    }

    if args.Period != "" {
        args.Period = strings.ToUpper(args.Period)
        if !core.TimeframeRegx.MatchString(args.Period) {
            err = fmt.Errorf("invalid timeframe value: %s", args.Period)
            return nil, err
        }
        opt.Periods = args.Period
    }

    return &opt, nil
}

// NewOutputs create timeframe instance
//
func NewOutputs(opt *AppOption) []core.Converter {
    outs := make([]core.Converter, 0)
    for _, period := range strings.Split(opt.Periods, ",") {
        var format core.Converter
        timeframe, _ := core.ParseTimeframe(strings.Trim(period, " \t\r\n"))

        switch opt.Format {
        case "csv":
            format = csv.New(opt.Start, opt.End, opt.CsvHeader, opt.Symbol, opt.Folder)
            break
        case "fxt":
            format = fxt4.NewFxtFile(timeframe, opt.Spread, opt.Mode, opt.Folder, opt.Symbol)
            break
        case "hst":
            format = hst.NewHST(timeframe, opt.Spread, opt.Symbol, opt.Folder)
            break
        default:
            log.Error("unsupported format %s.", opt.Format)
            return nil
        }

        outs = append(outs, core.NewTimeframe(period, opt.Symbol, format))
    }
    return outs
}

// NewApp create an application instance by input arguments
//
func NewApp(opt *AppOption) *DukaApp {
    return &DukaApp{
        option:  *opt,
        outputs: NewOutputs(opt),
    }
}

type hReader struct {
    Bi5  *bi5.Bi5
    DayH time.Time
    Data []byte
}

// Execute download source bi5 tick data from dukascopy
//
func (app *DukaApp) Execute() error {
    var (
        err       error
        opt       = app.option
        startTime = time.Now()
    )

    if len(app.outputs) < 1 {
        log.Error("No valid output format")
        return errors.New("no valid output format")
    }

    //
    // 创建输出目录
    //
    if _, err := os.Stat(opt.Folder); os.IsNotExist(err) {
        if err = os.MkdirAll(opt.Folder, 666); err != nil {
            log.Error("Create folder (%s) failed: %v.", opt.Folder, err)
            return err
        }
    }

    //
    // 按天下载，每天24小时的数据由24个goroutine并行下载
    //
    for day := opt.Start; day.Unix() < opt.End.Unix(); day = day.Add(24 * time.Hour) {
        //
        //  周六没数据，跳过
        //
        if day.Weekday() == time.Saturday {
            log.Warn("Skip Saturday %s.", day.Format("2006-01-02"))
            continue
        }
        //
        // 下载，解析，存储
        //
        if err = app.saveData(day, app.fetchDay(day)); err != nil {
            break
        }

        log.Info("%s %s finished.", opt.Symbol, day.Format("2006-01-02"))
    }

    //
    //  flush all output file
    //
    var wg sync.WaitGroup
    for _, output := range app.outputs {
        wg.Add(1)
        go func(o core.Converter) {
            defer wg.Done()
            o.Finish()
        }(output)
    }

    wg.Wait()
    log.Info("Time cost: %v.", time.Since(startTime))
    return err
}

// fetchDay 现在一天24小时的tick数据，24个goroutine并行下载，返回数据并不一定按时间顺序排序
// 转换端需要按天对tick数据排序。
//
func (app *DukaApp) fetchDay(day time.Time) <-chan *hReader {
    ch := make(chan *hReader, 24)
    opt := app.option

    go func() {
        defer close(ch)
        var wg sync.WaitGroup

        for hour := 0; hour < 24; hour++ {
            wg.Add(1)
            go func(h int) {
                defer wg.Done()
                dayH := day.Add(time.Duration(h) * time.Hour)
                bi5File := bi5.New(dayH, opt.Symbol, opt.Folder)

                var (
                    str  string
                    err  error
                    data []byte
                )
                if opt.Local {
                    str = "Load Bi5"
                    data, err = bi5File.Load()
                } else {
                    str = "Download Bi5"
                    data, err = bi5File.Download()
                }

                if err != nil {
                    log.Error("%s, %s failed: %v.", str, dayH.Format("2006-01-02:15H"), err)
                    return
                }
                if len(data) > 0 {
                    select {
                    case ch <- &hReader{Data: data[:], DayH: dayH, Bi5: bi5File}:
                        //log.Trace("%s %s", str, dayH.Format("2006-01-02:15H"))
                        break
                    }
                }
            }(hour)
        }

        wg.Wait()
        log.Trace("%s %s loaded.", opt.Symbol, day.Format("2006-01-02"))
    }()

    return ch
}

// sortAndOutput 按时间戳，从前到后排序当天tick数据
//
func (app *DukaApp) sortAndOutput(day time.Time, ticks []*core.TickData) error {
    if len(ticks) == 0 {
        return nil
    }

    // sort
    sort.Slice(ticks, func(i, j int) bool {
        return ticks[i].Timestamp < ticks[j].Timestamp
    })

    // 输出到文件
    for _, out := range app.outputs {
        timestamp := uint32(day.Unix())
        out.PackTicks(timestamp, ticks[:])
    }

    //firstTick := ticks[0].Timestamp
    //tm := time.Unix(firstTick/1000, 0).UTC()
    //log.Trace("%s sort and output day %v.", app.option.Format, tm)
    return nil
}

// saveData
func (app *DukaApp) saveData(day time.Time, chData <-chan *hReader) error {
    var (
        err error
        opt = app.option
    )

    nDay := -1
    dayTicks := make([]*core.TickData, 0, 2048)

    for data := range chData {
        // save bi5 by hour
        bi5File := data.Bi5
        var ticks []*core.TickData

        // 解析 bi5 成 TickData 数据
        if ticks, err = bi5File.Decode(data.Data[:]); err != nil {
            log.Error("Decode bi5 %s: %s failed: %v.", opt.Symbol, data.DayH.Format("2006-01-02:15H"), err)
            continue
        }

        // 保留 bi5 数据
        if err := bi5File.Save(data.Data[:]); err != nil {
            log.Error("Save Bi5 %s: %s failed: %v.", opt.Symbol, data.DayH.Format("2006-01-02:15H"), err)
            continue
        }

        // 新的一天开始
        if nDay != day.Day() {
            app.sortAndOutput(day, dayTicks[:])
            dayTicks = dayTicks[:0]
            nDay = day.Day()
        }

        dayTicks = append(dayTicks, ticks...)
    }

    if len(dayTicks) > 0 {
        app.sortAndOutput(day, dayTicks[:])
    }

    log.Trace("%s %s converted.", opt.Symbol, day.Format("2006-01-02"))
    return err
}
