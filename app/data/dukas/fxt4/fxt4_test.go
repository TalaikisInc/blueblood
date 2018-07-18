package fxt4

import (
    "bytes"
    "encoding/binary"
    "fmt"
    "io"
    "os"
    "testing"

    "github.com/adyzng/go-duka/core"
)

func TestFxtFile(t *testing.T) {
    fn := 1e-5 + 0.123
    fmt.Println(fn)

    fxt := NewFxtFile(1, 20, 0, "D:\\Data", "EURUSD")
    fxt.PackTicks(0, []*core.TickData{&core.TickData{}})
}

func TestHeader(t *testing.T) {
    fname := `F:\201209\EURUSD15_0.fxt`
    //fname := `F:\201710\EURUSD1.fxt`
    //fname := `C:\Users\huan\AppData\Roaming\MetaQuotes\Terminal\1DAFD9A7C67DC84FE37EAA1FC1E5CF75\tester\history\org\EURUSD15_0.fxt`

    fh, err := os.OpenFile(fname, os.O_RDONLY, 666)
    if err != nil {
        t.Fatalf("Open fxt file failed: %v.\n", err)
    }
    defer fh.Close()

    bs := make([]byte, headerSize)
    n, err := fh.Read(bs[:])
    if err != nil || n != headerSize {
        t.Fatalf("Read fxt header failed: %v.\n", err)
    }

    var h FXTHeader
    err = binary.Read(bytes.NewBuffer(bs[:]), binary.LittleEndian, &h)
    if err != nil {
        t.Fatalf("Decode fxt header failed: %v.\n", err)
    }

    fmt.Printf("Header:\n%+v\n", h)

    tickBs := make([]byte, tickSize)
    for {
        n, err = fh.Read(tickBs[:tickSize])
        if err == io.EOF {
            break
        }

        if n != tickSize || err != nil {
            t.Errorf("Read tick data failed: %v.\n", err)
            break
        }

        var tick FxtTick
        err = binary.Read(bytes.NewBuffer(tickBs[:]), binary.LittleEndian, &tick)
        if err != nil {
            t.Errorf("Decode tick data failed: %v.\n", err)
            break
        }

        fmt.Printf("%+v\n", tick)
        //break
    }
}
