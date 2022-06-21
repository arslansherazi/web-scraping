import logging

from scrapy.signalmanager import dispatcher
from scrapy import signals
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner

from scraper.spiders.beauty_products import BeautyProductsSpider
from scraper.spiders.laptops_details import LaptopsDetailsSpider

logger = logging.getLogger('logs')


class RunSpiders(object):
    def __init__(self):
        self.runner = CrawlerRunner(get_project_settings())

    @staticmethod
    def crawler_results(signal, sender, item, response, spider):
        logger.info(item)

    @staticmethod
    def spider_opened(spider):
        """
        Triggers and save logs in db when any spider is called

        :param spider: spider
        """
        spider_name = spider.name.capitalize()
        message = f"{spider_name} spider started successfully"
        logger.info(message)

    @staticmethod
    def spider_closed(spider, reason):
        """
        Triggers and save logs in db when any spider is finished its processing

        :param spider: spider
        :param str reason: reason
        """
        spider_name = spider.name.capitalize()
        message = f'{spider_name} crawler ended successfully'
        if reason != 'finished':
            message = f'{spider_name} crawler ended with error(s)'
        logger.info(message)

    def run(self):
        yield self.runner.crawl(BeautyProductsSpider)
        yield self.runner.crawl(LaptopsDetailsSpider)
        reactor.stop()


def dispatch_signals():
    """
    Dispatches crawler signals
    """
    dispatcher.connect(RunSpiders.spider_opened, signal=signals.spider_opened)
    dispatcher.connect(RunSpiders.spider_closed, signal=signals.spider_closed)
    dispatcher.connect(RunSpiders.crawler_results, signal=signals.item_passed)


if __name__ == '__main__':
    dispatch_signals()
    RunSpiders().run()
    reactor.run()
