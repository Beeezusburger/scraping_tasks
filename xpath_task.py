import os

import pandas as pd
import pendulum
from lxml import html
from price_parser import parse_price


#TODO ask about prices and number of rows
def parse(file, requested_item):
    page_tree = load_html_tree(file)
    item = extract_data(page_tree)
    scraped_item = pd.DataFrame.from_records([item])
    return scraped_item.equals(requested_item)

def extract_data(page_tree):
    return{
        'artist_name': extract_name(page_tree),
        'painting_name': parse_xpath(page_tree, '//h2[@class="itemName"]/i/text()'),
        'price_gbp': extract_price(page_tree, 'RealizedPrimary'),
        'price_usd': extract_price(page_tree, 'RealizedSecondary'),
        'estimates_gbp': extract_estimates(page_tree, 'PriceEstimatedPrimary'),
        'estimates_usd': extract_estimates(page_tree, 'PriceEstimatedSecondary'),
        'image_url': parse_xpath(page_tree, '//img[@id="imgLotImage"]/@src'),
        'sale_date': extract_sale_date(page_tree)
    }

def extract_name(page_tree):
    artist_data = parse_xpath(page_tree, '//h1[@class="lotName"]/text()')
    artist_name = artist_data.split('(')
    return artist_name[0] if artist_name else ''

def extract_price(page_tree, category):
    price_data = find_price_by_category(page_tree, category, 0)
    price = parse_price(price_data)
    return price.amount_float

def extract_estimates(page_tree, category):
    price_data = find_price_by_category(page_tree, category)
    if not price_data:
        return ''
    estimates_data = price_data.split('-')
    estimates = [parse_price(price).amount_text for price in estimates_data]
    return (' - ').join(estimates) if estimates else ''

def find_price_by_category(page_tree, category, default=''):
    path = (
        f'//span[contains(@id, "{category}")]/text()'
        f' | //div[contains(@id, "{category}")]/text()'
    )
    return parse_xpath(page_tree, path, default)

def extract_sale_date(page_tree):
    date = parse_xpath(page_tree, '//span[contains(@id, "SaleDate")]/text()')
    dt = pendulum.parse(date, strict=False)
    return dt.format('YYYY-MM-DD') if dt else ''

def load_html_tree(file):
    with open(file, "r") as f:
        page = f.read()
    return html.fromstring(page)

def parse_xpath(page_tree, path, default_value=''):
    data = page_tree.xpath(path)
    return data[0] if data else default_value


if __name__ == "__main__":
    file = os.path.join('candidate_eval_data', 'webpage.html')
    requested_item = pd.DataFrame([{
        'artist_name': 'Peter Doig ',
        'painting_name': "The Architect's Home in the Ravine ",
        'price_gbp': 11282500.0,
        'price_usd': 16370908.0,
        'estimates_gbp': '10,000,000 - 15,000,000',
        'estimates_usd': '14,509,999 - 21,764,999',
        'image_url': 'http://www.christies.com/lotfinderimages'
                     '/D59730/peter_doig_the_architects_home_in_the_ravine_d5973059g.jpg',
        'sale_date': '2016-02-11'
    }])
    print(parse(file, requested_item))