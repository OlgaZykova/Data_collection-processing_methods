from scrapy.settings import Settings
from leroymerlinparser import settings
from scrapy.crawler import CrawlerProcess
from leroymerlinparser.spiders.leroymerlinru import LeroymerlinruSpider
from sys import argv

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(LeroymerlinruSpider,search = argv[1])
    process.start()
