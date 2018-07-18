package core

// Downloader interface...
type Downloader interface {
    Download(URL string) ([]byte, error)
}
