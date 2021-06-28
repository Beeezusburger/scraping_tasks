from twisted.web.http_headers import Headers as TwistedHeaders


class HeadersOrder(object):

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings)
        return obj

    @staticmethod
    def monkey_patch_twisted_headers(order):
        def getAllRawHeaders(self):
            for k, v in sorted(
                    self._rawHeaders.items(),
                    key=lambda x: order.index(x[0]) if x[0] in order else 1000
            ):
                yield self._canonicalNameCaps(k), v

        TwistedHeaders.getAllRawHeaders = getAllRawHeaders

    def __init__(self, settings):
        self.monkey_patch_twisted_headers(settings['HEADERS_ORDER'])