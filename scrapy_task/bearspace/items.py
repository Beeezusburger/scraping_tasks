import scrapy


class BearspaceLot(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    media = scrapy.Field()
    height_cm = scrapy.Field()
    width_cm = scrapy.Field()
    price_gbp= scrapy.Field()