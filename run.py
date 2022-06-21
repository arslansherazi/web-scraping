import logging

from scrapy.signalmanager import dispatcher
from scrapy import signals
from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from scraper.spiders.laptops_details import LaptopsDetailsSpider

logger = logging


def run():
    runner = CrawlerRunner(get_project_settings())
    configure_logging()

    def crawler_results(signal, sender, item, response, spider):
        logger.info(item)

    def spider_opened(spider):
        """
        Triggers and save logs in db when any spider is called
        :param spider: spider
        """
        spider_name = spider.name.capitalize()
        message = f"{spider_name} crawler started successfully"
        logger.info(message)

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

    dispatcher.connect(spider_opened, signal=signals.spider_opened)
    dispatcher.connect(spider_closed, signal=signals.spider_closed)
    dispatcher.connect(crawler_results, signal=signals.item_passed)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(BeautyProductsSpider)
        yield runner.crawl(LaptopsDetailsSpider)
        reactor.stop()
    crawl()
    reactor.run()


if __name__ == '__main__':
    run()
