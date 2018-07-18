package misc

import (
    "bytes"
    "encoding/binary"
    "errors"
    "strings"
)

// ToFixBytes convert string to fix bytes array
//
func ToFixBytes(bs []byte, s string) (int, error) {
    r := strings.NewReader(s)
    return r.Read(bs[:])
}

// PackLittleEndian serialize `val` into bytes with LittleEndian
//
func PackLittleEndian(size int, v interface{}) ([]byte, error) {
    if size == 0 || v == nil {
        return nil, errors.New("invalid arguments")
    }
    bu := bytes.NewBuffer(make([]byte, 0, size))
    if err := binary.Write(bu, binary.LittleEndian, v); err != nil {
        return nil, err
    }
    return bu.Bytes(), nil
}

// PackBigEndian serialize `val` into bytes with BigEndian
//
func PackBigEndian(size int, v interface{}) ([]byte, error) {
    if size == 0 || v == nil {
        return nil, errors.New("invalid arguments")
    }
    bu := bytes.NewBuffer(make([]byte, 0, size))
    if err := binary.Write(bu, binary.BigEndian, v); err != nil {
        return nil, err
    }
    return bu.Bytes(), nil
}
