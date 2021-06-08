from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from booksearch import settings
from booksearch.spiders.labirintru import LabirintruSpider
from booksearch.spiders.book24ru import Book24ruSpider
if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabirintruSpider)
    process.crawl(Book24ruSpider)
    process.start()
