package bi5

import (
    "bytes"
    "encoding/binary"
    "errors"
    "fmt"
    "io"
    "io/ioutil"
    "os"
    "path/filepath"
    "time"

    "github.com/adyzng/go-duka/core"
    "github.com/adyzng/go-duka/misc"
    "github.com/kjk/lzma"
)

var (
    ext         = "bi5"
    log         = misc.NewLogger("Bi5", 3)
    normSymbols = []string{"USDRUB", "XAGUSD", "XAUUSD"}
    httpDownld  = core.NewDownloader()
    emptBytes   = make([]byte, 0)
)

const (
    TICK_BYTES = 20
)

// Bi5 from dukascopy
type Bi5 struct {
    dayH   time.Time
    symbol string
    dest   string
    save   bool
}

// New create an bi5 saver
func New(day time.Time, symbol, dest string) *Bi5 {
    y, m, d := day.Date()
    dir := fmt.Sprintf("%s/%04d/%02d/%02d", symbol, y, m, d)

    return &Bi5{
        dest:   filepath.Join(dest, dir),
        dayH:   day,
        symbol: symbol,
    }
}

// Decode bi5 to tick data array
//
func (b *Bi5) Decode(data []byte) ([]*core.TickData, error) {
    dec := lzma.NewReader(bytes.NewBuffer(data[:]))
    defer dec.Close()

    ticksArr := make([]*core.TickData, 0)
    bytesArr := make([]byte, TICK_BYTES)

    for {
        n, err := dec.Read(bytesArr[:])
        if err == io.EOF {
            err = nil
            break
        }
        if n != TICK_BYTES || err != nil {
            log.Error("LZMA decode failed: %d: %v.", n, err)
            break
        }

        t, err := b.decodeTickData(bytesArr[:], b.symbol, b.dayH)
        if err != nil {
            log.Error("Decode tick data failed: %v.", err)
            break
        }

        ticksArr = append(ticksArr, t)
    }

    return ticksArr, nil
}

// Save bi5 data to file
//
func (b *Bi5) Save(data []byte) error {
    if len(data) == 0 || !b.save {
        return nil
    }

    if err := os.MkdirAll(b.dest, 666); err != nil {
        log.Error("Create folder (%s) failed: %v.", b.dest, err)
        return err
    }

    fname := fmt.Sprintf("%02dh.%s", b.dayH.Hour(), ext)
    fpath := filepath.Join(b.dest, fname)

    f, err := os.OpenFile(fpath, os.O_CREATE|os.O_TRUNC|os.O_RDWR, 666)
    if err != nil {
        log.Error("Create file %s failed: %v.", fpath, err)
        return err
    }

    defer f.Close()
    len, err := f.Write(data[:])
    if err == nil {
        log.Trace("Saved file %s => %d.", fpath, len)
    } else {
        log.Error("Write file %s failed: %v.", fpath, err)
    }
    return err
}

// Load bi5 data from file content
//
func (b *Bi5) Load() ([]byte, error) {

    fname := fmt.Sprintf("%02dh.%s", b.dayH.Hour(), ext)
    fpath := filepath.Join(b.dest, fname)

    f, err := os.OpenFile(fpath, os.O_RDONLY, 666)
    if err != nil {
        if os.IsNotExist(err) {
            log.Trace("Bi5 (%s) not exist, try to download from dukascopy", fpath)
            return b.Download()
        }
        log.Error("Open file %s failed: %v.", fpath, err)
        return nil, err
    }

    defer f.Close()
    return ioutil.ReadAll(f)
}

// Download from dukascopy
//
func (b *Bi5) Download() ([]byte, error) {
    var (
        err  error
        data []byte
    )

    year, month, day := b.dayH.Date()
    // !! 注意: month - 1
    link := fmt.Sprintf(core.DukaTmplURL, b.symbol, year, month-1, day, b.dayH.Hour())

    if data, err = httpDownld.Download(link); err != nil {
        log.Error("%s %s download failed: %v.", b.symbol, b.dayH.Format("2006-01-02:15H"), err)
        return emptBytes, err
    }

    if len(data) > 0 {
        log.Trace("%s %s downloaded.", b.symbol, b.dayH.Format("2006-01-02:15H"))
        b.save = true
        return data, err
    }

    log.Warn("%s %s empty.", b.symbol, b.dayH.Format("2006-01-02:15H"))
    return emptBytes, nil
}

// decodeTickData from input data bytes array.
// the valid data array should be at size `TICK_BYTES`.
//
//  struck.unpack(!IIIff)
//  date, ask / point, bid / point, round(volume_ask * 100000), round(volume_bid * 100000)
//
func (b *Bi5) decodeTickData(data []byte, symbol string, timeH time.Time) (*core.TickData, error) {
    raw := struct {
        TimeMs    int32 // millisecond offset of current hour
        Ask       int32
        Bid       int32
        VolumeAsk float32
        VolumeBid float32
    }{}

    if len(data) != TICK_BYTES {
        return nil, errors.New("invalid length for tick data")
    }

    buf := bytes.NewBuffer(data)
    if err := binary.Read(buf, binary.BigEndian, &raw); err != nil {
        return nil, err
    }

    var point float64 = 100000
    for _, sym := range normSymbols {
        if symbol == sym {
            point = 1000
            break
        }
    }

    t := core.TickData{
        Symbol:    symbol,
        Timestamp: timeH.Unix()*1000 + int64(raw.TimeMs), //timeH.Add(time.Duration(raw.TimeMs) * time.Millisecond),
        Ask:       float64(raw.Ask) / point,
        Bid:       float64(raw.Bid) / point,
        VolumeAsk: float64(raw.VolumeAsk),
        VolumeBid: float64(raw.VolumeBid),
    }

    return &t, nil
}
