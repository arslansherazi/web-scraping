import scrapy


class BeautyProduct(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    rating = scrapy.Field()
    total_ratings = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()


class LaptopDetails(scrapy.Item):
    details = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()
