#!/bin/bash

go get github.com/adyzng/go-duka/...
go build
go-duka -format csv -start "2016-01-01" -symbol EURUSD -timeframe M15 -verbose -header -output "../../../storage"
