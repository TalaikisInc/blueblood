package hst

import (
    "bytes"
    "encoding/binary"
    "encoding/csv"
    "io"
    "os"
    "testing"
)

func TestHSTHeader(t *testing.T) {
    header := NewHeader(1, "EURUSD")

    bs, _ := header.ToBytes()
    if len(bs) != headerBytes {
        t.Errorf("Encode header failed: %d, %x.\n", len(bs), bs)
    } else {
        var h Header
        err := binary.Read(bytes.NewBuffer(bs), binary.LittleEndian, &h)

        if err != nil {
            t.Errorf("Decode header failed: %v.\n", err)
        }

        t.Logf("%+v.\n", h)
        t.Logf("Copyright: %s, Symbol: %s\n", string(h.Copyright[:]), string(h.Symbol[:]))
    }
}

func TestLoadHst(t *testing.T) {

    fcsv := `F:\201710\EURUSD1.hst.csv`
    fname := `F:\201710\EURUSD1.hst`
    //fname := "C:\\Users\\huan\\AppData\\Roaming\\MetaQuotes\\Terminal\\1DAFD9A7C67DC84FE37EAA1FC1E5CF75\\history\\ICMarkets-Demo01\\00\\EURUSD30.hst"

    f, err := os.OpenFile(fname, os.O_RDONLY, 666)
    if err != nil {
        t.Fatalf("Open file error: %v.\n", err)
    }

    defer f.Close()
    bs := make([]byte, headerBytes)

    n, err := f.Read(bs[:])
    if n != headerBytes || err != nil {
        t.Fatalf("Load file header failed: %v.\n", err)
    }

    var h Header
    err = binary.Read(bytes.NewBuffer(bs[:]), binary.LittleEndian, &h)
    if err != nil {
        t.Errorf("Decode header failed: %v.\n", err)
    }

    t.Logf("%+v.\n", h)
    t.Logf("Copyright: %s, Symbol: %s\n", string(h.Copyright[:]), string(h.Symbol[:]))

    // open csv
    fc, err := os.OpenFile(fcsv, os.O_CREATE|os.O_TRUNC|os.O_RDWR, 666)
    if err != nil {
        t.Errorf("Failed to create file %s, error %v.\n", fcsv, err)
    }

    wc := csv.NewWriter(fc)

    defer func() {
        fc.Close()
        wc.Flush()
    }()

    barCount := 0
    barBs := make([]byte, barBytes)
    for {
        barBs = barBs[:barBytes]
        n, err := f.Read(barBs[:])

        if err == io.EOF {
            break
        }

        if n != barBytes || err != nil {
            t.Errorf("Read bar data failed: %d:%v.\n", n, err)
            break
        }

        var bar BarData
        err = binary.Read(bytes.NewBuffer(barBs[:]), binary.LittleEndian, &bar)
        if err != nil {
            t.Errorf("Decode bar data failed: %v.\n", err)
            break
        }

        wc.Write(bar.Strings())
        //t.Logf("Bar %d: %+v\n", barCount, bar)
        barCount++
    }
}
