import scrapy
from scrapy.http import HtmlResponse
from leroymerlinparser.items import LeroymerlinparserItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    # поисковый запрос задаем в параметрах командной строки при запуске
    def __init__(self, search):
        super(LeroymerlinruSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}&page=1']

    def parse(self, response: HtmlResponse):
        #ограничиваю перебор страниц, ибо очень долго
        max_page_number = 20
        goods_links = response.xpath("//div[@data-qa-product]//a")
        next_page = response.xpath("//a[contains(@aria-label,'Следующая страница')]/@href").extract_first()
        #вот тут получаю номер текущей страницы
        tmp = response.url.split(sep='=')
        page_number = int(tmp[-1])
        #здесь проверка номера страницы добавлена
        if next_page and page_number <= max_page_number:
            yield response.follow('https://leroymerlin.ru' + next_page, callback=self.parse)
        for link in goods_links:
            yield response.follow(link, callback=self.good_parse)

    def good_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//uc-pdp-price-view[@slot='primary-price']//span[@slot]/text()")
        loader.add_xpath('params', "//div[@class='def-list__group']//text()")
        loader.add_xpath('photos', "//img[@slot='thumbs']/@src")
        loader.add_value('link', response.url)
        yield loader.load_item()
