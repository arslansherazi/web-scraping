import json
from time import sleep

import scrapy
from scrapy.http.headers import Headers
import logging

from scraper.items import BeautyProduct

RENDER_HTML_URL = "http://127.0.0.1:8050/render.html"

logger = logging.getLogger('logs')


class BeautyProductsSpider(scrapy.Spider):
    name = 'beauty_products'
    allowed_domains = ['amazon.com']
    start_urls = [
        'https://www.amazon.com/s?i=beauty-intl-ship&rh=n%3A16225006011&fs=true&page=1&qid=1649621337&ref=sr_pg_1'
    ]
    custom_settings = {
        "ITEM_PIPELINES": {"scraper.pipelines.BeautyProductsPipeline": 100}
    }

    def __init__(self):
        super().__init__()
        for page_no in range(2, 401):
            product_page_link = f'https://www.amazon.com/s?i=beauty-intl-ship&rh=n%3A16225006011&fs=true&page={page_no}&qid=1649621337&ref=sr_pg_{page_no}'
            self.start_urls.append(product_page_link)

    def start_requests(self):
        for url in self.start_urls:
            body = json.dumps({"url": url, "wait": 0.5}, sort_keys=True)
            headers = Headers({'Content-Type': 'application/json'})
            yield scrapy.Request(RENDER_HTML_URL, self.parse, method="POST", body=body, headers=headers)
            sleep(2)

    def parse(self, response, **kwargs):
        try:
            products_data = response.xpath(
                '//div[contains(@class, "a-section") and contains(@class, "a-spacing-base")]'
            )
            for product_data in products_data:
                try:
                    beauty_product = BeautyProduct()
                    beauty_product['name'] = product_data.xpath('div/div/h2/a/span/text()').extract_first()
                    beauty_product['description'] = product_data.xpath('div/div/div/div/div/span/text()').extract_first()
                    product_rating = product_data.xpath('div/div/div/span/span/a/i/span/text()').extract_first()
                    beauty_product['rating'] = 0.0
                    if product_rating:
                        beauty_product['rating'] = float(product_rating.split(' ')[0])
                    beauty_product['total_ratings'] = int(
                        product_data.xpath('div/div/div/span/a/span/text()').extract_first().replace(',', '')
                    )
                    beauty_product['price'] = product_data.xpath('div/div/div/a/span/span/text()').extract_first()
                    beauty_product['image_url'] = product_data.xpath('div/span/a/div/img/@src').extract_first()
                    yield beauty_product
                except Exception as e:
                    logger.error("Exception occurred at item level")
                    continue
        except Exception as e:
            logger.error("Exception occurred at page")
