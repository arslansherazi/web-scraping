from time import sleep

import scrapy

from scraper.db import insert_laptop_details


class LaptopsDetailsSpider(scrapy.Spider):
    name = 'laptops_details'
    allowed_domains = ['www.priceoye.pk']
    start_urls = [
        'https://priceoye.pk/laptops?page=1',
        'https://priceoye.pk/laptops?page=2',
        'https://priceoye.pk/laptops?page=3',
        'https://priceoye.pk/laptops?page=4'
    ]

    def parse(self, response):
        laptops_data = response.xpath('//div[@class="detail-box"]')
        laptops_images = response.xpath('//div[@class="image-box"]')
        for laptop_data, laptop_image in zip(laptops_data, laptops_images):
            try:
                laptop_name = laptop_data.xpath('h4[@class="p3"]/text()').extract()[0].strip()
                laptop_price = laptop_data.xpath('div[@class="price-box"]/text()').extract()[0].strip().split(' ')[1]
                laptop_image_url = laptop_image.xpath('amp-img/amp-img/@src').extract()[0]
                insert_laptop_details(laptop_name, laptop_price, laptop_image_url)
                sleep(1)
            except Exception as e:
                continue
