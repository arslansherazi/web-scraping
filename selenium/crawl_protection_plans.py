from selenium import webdriver
from scrapy.selector import Selector


class CrawlProtectionPlans(object):

    def __init__(self):
        self.driver = webdriver.Firefox(executable_path='./geckodriver')

    def crawl(self):
        self.driver.get('https://www.newegg.com/lg-c1-65/p/N82E16889007772')
        selector = Selector(text=self.driver.page_source)
        protection_plans = selector.xpath(
            '//div[@class="product-protection"]/div[@class="items-list-view"]/div/div[@class="item-action"]/label'
        )

        for protection_plan in protection_plans:
            protection_plan_title = protection_plan.xpath('span/text()').extract_first()
            print(protection_plan_title)


if __name__ == '__main__':
    CrawlProtectionPlans().crawl()
