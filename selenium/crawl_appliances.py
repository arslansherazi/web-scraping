from seleniumwire import webdriver
from scrapy.selector import Selector
import psycopg2
from selenium.webdriver.support.ui import WebDriverWait


class CrawlAppliances(object):
    def __init__(self):
        proxy_options = {
            'proxy': {
                'http': 'http://scraperapi:03aa49b7a3c89dc53729d8bb52df37e3@proxy-server.scraperapi.com:8001',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
        self.driver = webdriver.Chrome(executable_path='./chromedriver', seleniumwire_options=proxy_options)
        self.connection = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password="postgres",
            dbname="postgres"
        )
        self.cursor = self.connection.cursor()

    def crawl(self):
        WebDriverWait(self.driver, 10)
        self.driver.get('https://www.homedepot.com/b/Appliances-Mini-Fridges/N-5yc1vZc4mo')
        selector = Selector(text=self.driver.page_source)
        items_data_sections = selector.xpath('//div[@class="results-wrapped"]/div/section')
        for items_data_section in items_data_sections:
            items_data = items_data_section.xpath('div')
            for item_data in items_data:
                item_url = item_data.xpath(
                    'div/div[@class="product-pod--padding"]/div[@class="product-pod__title product-pod__title__product"]/a/@href' # noqa: 501
                ).extract_first()
                if not item_url:
                    item_url = item_data.xpath(
                        'div/div[@class="product-pod--padding"]/div[@class="product-pod__title"]/a/@href'
                    ).extract_first()
                item_name = item_data.xpath(
                    'div/div[@class="product-pod--padding"]/div[@class="product-pod__title product-pod__title__product"]/a/div/h2/span[@class="product-pod__title__product"]/text()' # noqa: 501
                ).extract_first()
                if not item_name:
                    item_name = item_data.xpath(
                        'div/div[@class="product-pod--padding"]/div[@class="product-pod__title"]/a/div/h2/span[@class="product-pod__title__product"]/text()' # noqa: 501
                    ).extract_first()

                if not item_url or not item_name:
                    continue

                self.add_item_into_db(item_name, item_url)

    def add_item_into_db(self, name, url):
        try:
            query = """
                INSERT INTO appliance (name, url) 
                VALUES (%s, %s)
            """
            self.cursor.execute(query, (
                name,
                url
            ))
            self.connection.commit()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    CrawlAppliances().crawl()
