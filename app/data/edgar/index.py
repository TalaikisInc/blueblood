from SECEdgar.crawler import SecCrawler

crawler = SecCrawler()


def get(symbol):
    crawler.filing_10Q(symbol, '0000320193', '20010101', '10')

# http://rankandfiled.com/#/data/tickers