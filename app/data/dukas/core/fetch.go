package core

import (
    "fmt"
    "io/ioutil"
    "net/http"
    "time"

    "github.com/adyzng/go-duka/misc"
)

const (
    // "https://datafeed.dukascopy.com/datafeed/{currency}/{year}/{month:02d}/{day:02d}/{hour:02d}h_ticks.bi5"
    DukaTmplURL = "https://datafeed.dukascopy.com/datafeed/%s/%04d/%02d/%02d/%02dh_ticks.bi5"
    retryTimes  = 5
)

var (
    log = misc.NewLogger("Duka", 2)
)

type HTTPDownload struct {
    client *http.Client
}

func NewDownloader() Downloader {
    return &HTTPDownload{
        client: &http.Client{
            Timeout: 5 * time.Minute,
        },
    }
}

func (h *HTTPDownload) Download(URL string) ([]byte, error) {
    var err error
    for retry := 0; retry < retryTimes; retry++ {
        var resp *http.Response
        resp, err = h.client.Get(URL)
        if err != nil {
            log.Error("[%d] Download %s failed: %v.", retry, URL, err)
            continue
        }
        defer resp.Body.Close()

        if resp.StatusCode != http.StatusOK {
            log.Warn("[%d] Download %s failed %d:%s.", retry, URL, resp.StatusCode, resp.Status)
            if resp.StatusCode == http.StatusNotFound {
                // 404
                break
            }
            err = fmt.Errorf("http error %d:%s", resp.StatusCode, resp.Status)
            continue
        }

        data, err := ioutil.ReadAll(resp.Body)
        return data, err
    }
    return nil, err
}
