# -*- coding: utf-8 -*-
import re
from urllib.parse import urljoin

import chompjs
import jmespath
import scrapy
import w3lib.html
from w3lib.url import add_or_replace_parameter

from ..items import BearspaceLot


class BearspaceLotsSpider(scrapy.Spider):
    name = 'bearspace_lots'
    allowed_domains = ['bearspace.co.uk']
    BASE_URL = 'https://www.bearspace.co.uk/product-page/'
    LOTS_PER_PAGE = 10

    def start_requests(self):
        url = 'https://www.bearspace.co.uk/purchase'
        yield scrapy.Request(
            url=url,
            callback=self.total_count_callback
        )

    def total_count_callback(self, response):
        # Last page of pagination will contain inline js-like object
        # that will contain the data of all products except media.
        total_lots_count = self.parse_total_count(response)
        if not total_lots_count:
            return

        total_pages = total_lots_count / self.LOTS_PER_PAGE
        max_lots_page_url = add_or_replace_parameter(response.url, 'page', total_pages)
        last_page_request = scrapy.Request(
            url=max_lots_page_url,
            callback=self.scrape_lots_callback
        )
        yield last_page_request

    def scrape_lots_callback(self, response):
        script_text = self.parse_script_text(response)
        try:
            json_data = chompjs.parse_js_object(script_text)
        except ValueError:
            self.log('Failed to extract data from {}'.format(response.url))
            return
        lots = self.extract_lots(json_data)

        for lot in lots or []:
            lot_data = self.parse_lot_data(lot)
            if not lot_data.get('url'):
                continue

            lot_media_request = scrapy.Request(
                url=lot_data.get('url'),
                callback=self.lot_media_callback,
                meta={'lot_data': lot_data}
            )
            yield lot_media_request

    def lot_media_callback(self, response):
        lot = response.meta.get('lot_data') or {}
        media = self.extract_media(response)
        bearspace_lot = BearspaceLot(
            url=lot.get('url'),
            title=lot.get('title'),
            height_cm=lot.get('height_cm'),
            width_cm=lot.get('width_cm'),
            price_gbp=lot.get('price_gbp'),
            media=media
        )
        yield bearspace_lot

    def extract_media(self, response):
        # TODO this might be the case to train SpaCy NER or use fuzzy lib
        # because of unsctructured html data
        path = '//pre[@data-hook="description"]/p'
        description_list = response.xpath(path).extract()
        return self.extract_media_from_description(description_list)

    def extract_media_from_description(self, description_list):
        media = [
            w3lib.html.remove_tags(item, which_ones=('p', 'span'))
            for item in description_list
            if not re.search(r'\d', item)
            and '\xa0' not in item
        ]
        return media[0] if media else ''

    def parse_lot_data(self, lot):
        return {
            'url': urljoin(self.BASE_URL, lot.get('urlPart')),
            'title': lot.get('name'),
            'height_cm' : jmespath.search('media[0].height', lot),
            'width_cm': jmespath.search('media[0].width', lot),
            'price_gbp': lot.get('price')
        }
    def extract_lots(self, json_data):
        expression = '*.*.*.catalog.category.productsWithMetaData.list[*] | [1] | [0] | [0]'
        return jmespath.search(expression, json_data)

    def parse_script_text(self, response):
        path = '//script[@id="wix-warmup-data"]/text()'
        return response.xpath(path).extract_first()

    def parse_total_count(self, response):
        path = '//script[@id="wix-warmup-data"]/text()'
        pattern = r'totalCount":(\d+)'
        total_count = response.xpath(path).re_first(pattern)
        return int(total_count) if total_count else None
