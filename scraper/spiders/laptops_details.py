import scrapy

from scraper.items import LaptopDetails


class LaptopsDetailsSpider(scrapy.Spider):
    name = 'laptops_details'
    allowed_domains = ['www.priceoye.pk']
    start_urls = [
        'https://priceoye.pk/laptops?page=1',
        'https://priceoye.pk/laptops?page=2',
        'https://priceoye.pk/laptops?page=3',
        'https://priceoye.pk/laptops?page=4'
    ]
    custom_settings = {
        "ITEM_PIPELINES": {"scraper.pipelines.LaptopDetailsPipeline": 100}
    }

    def parse(self, response, **kwargs):
        laptops_data = response.xpath('//div[@class="detail-box"]')
        laptops_images = response.xpath('//div[@class="image-box"]')
        for laptop_data, laptop_image in zip(laptops_data, laptops_images):
            try:
                laptop_details = LaptopDetails()
                laptop_details['details'] = laptop_data.xpath('h4[@class="p3"]/text()').extract()[0].strip()
                laptop_details['price'] = laptop_data.xpath(
                    'div[@class="price-box"]/text()'
                ).extract()[0].strip().split(' ')[1]
                laptop_details['image_url'] = laptop_image.xpath('amp-img/amp-img/@src').extract()[0]
                yield laptop_details
            except Exception as e:
                self.logger.error("Error occurred in laptop details")
