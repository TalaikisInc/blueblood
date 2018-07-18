package core

import (
    "io"
)

// Parser interface used to parse data
type Parser interface {
    Parse(r io.Reader) error
}

// Saver interface used to save data
type Saver interface {
    Save(r io.Reader) error
}

// Converter convert raw tick data into different file format
// such as fxt, hst, csv
type Converter interface {
    // PackTicks by timeframe M1,M5...
    // `barTimestamp` is the timeframe in seconds
    // `ticks` is all the ticks data within timeframe
    PackTicks(barTimestamp uint32, ticks []*TickData) error
    // Finish current timeframe
    Finish() error
}
