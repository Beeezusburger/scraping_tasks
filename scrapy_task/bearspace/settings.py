BOT_NAME = 'bearspace'

SPIDER_MODULES = ['bearspace.spiders']
NEWSPIDER_MODULE = 'bearspace.spiders'

USER_AGENT = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32

DEFAULT_REQUEST_HEADERS = {
    "Upgrade-Insecure-Requests": 1,
    "Accept": "text/html,application/xhtml+xml,application/xml"
              ";q=0.9,image/avif,image/webp,image/apng,*/*"
              ";q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive"
}

DOWNLOADER_MIDDLEWARES = {
    'bearspace.middlewares.HeadersOrder': 800,
}

HEADERS_ORDER = [
    b'host',
    b'connection',
    b'content-length',
    b'pragma',
    b'cache-control',
    b'upgrade-insecure-requests',
    b'origin',
    b'user-agent',
    b'dnt',
    b'content-type',
    b'accept',
    b'sec-fetch-site',
    b'sec-fetch-mode',
    b'sec-fetch-user',
    b'sec-fetch-dest',
    b'referer',
    b'x-requested-with',
    b'accept-encoding',
    b'accept-language',
    b'cookie',
    ]

ITEM_PIPELINES = {
    'bearspace.pipelines.BearspacePipeline': 300,
}
