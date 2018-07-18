package misc

import (
    "fmt"
    "strings"

    log "github.com/go-clog/clog"
)

// Logger interface
type Logger interface {
    Trace(format string, v ...interface{})
    Info(format string, v ...interface{})
    Warn(format string, v ...interface{})
    Error(format string, v ...interface{})
    Fatal(format string, v ...interface{})
}

// NewLogger create Logger instance with `prefix`, `skip` is used for `Error` and `Fatal` stack trace.
//   Example:
//        log := NewLogger("App", 2)
//
func NewLogger(prefix string, skip int) Logger {
    return &logPrefix{
        prefix: strings.ToTitle(prefix),
        skip:   skip,
    }
}

type logPrefix struct {
    prefix string
    skip   int
}

func (l *logPrefix) Trace(format string, v ...interface{}) {
    if l.prefix != "" {
        format = fmt.Sprintf("[%s] %s", l.prefix, format)
    }
    log.Trace(format, v...)
}

func (l *logPrefix) Info(format string, v ...interface{}) {
    if l.prefix != "" {
        format = fmt.Sprintf("[%s] %s", l.prefix, format)
    }
    log.Info(format, v...)
}

func (l *logPrefix) Warn(format string, v ...interface{}) {
    if l.prefix != "" {
        format = fmt.Sprintf("[%s] %s", l.prefix, format)
    }
    log.Warn(format, v...)
}

func (l *logPrefix) Error(format string, v ...interface{}) {
    if l.prefix != "" {
        format = fmt.Sprintf("[%s] %s", l.prefix, format)
    }
    log.Error(l.skip, format, v...)
}

func (l *logPrefix) Fatal(format string, v ...interface{}) {
    if l.prefix != "" {
        format = fmt.Sprintf("[%s] %s", l.prefix, format)
    }
    log.Fatal(l.skip, format, v...)
}
