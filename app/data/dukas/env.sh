#!/bin/bash

go get github.com/Adyzng/go-duka
go get github.com/adyzng/go-duka/...
go build
go-duka -format csv -start "2016-01-01" -symbol EURUSD -timeframe M15 -header -output "../../../storage/dukas"
go-duka -format csv -start "2016-01-01" -symbol GBPUSD -timeframe M15 -header -output "../../../storage/dukas"

# https://www.dukascopy.com/swiss/english/marketwatch/historical/