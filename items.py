# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose


# сама не особо поняла смысл этого изменения - размер картинки меняется, а качество нет, но "больших" картинок там не было
def change_url(value):
    result = value.replace('w_82', 'w_300')
    result = result.replace('h_82', 'h_300')
    return result


# преобразуем цену из списка в словарь
def concat_price(value):
    result = {}
    result['price'] = int(value[0].replace(' ', ''))
    result['cur'] = value[1]
    result['unit'] = value[2]
    return result


# здесь очистка характеристик товара от лишних найденных значений из списка
# предполагаю, что можно было как-то собирать так данные, чтобы в них не попадал мусор лишний, но времени не хватило
def clear_params(value):
    result = [value[i] for i in range(0, len(value) + 1) if i % 5 == 1 or i % 5 == 3]
    result = make_params(result)
    return result


# здесь избавляемся от лишних пробелов и пустых строк в значениях характеристик
def make_params(value):
    result = {}
    for i in range(0, len(value), 2):
        value[i + 1] = value[i + 1].replace(' \n            ', ' ')
        value[i + 1] = value[i + 1].replace('\n                ', ' ')
        result[value[i]] = value[i + 1]
    return result


class LeroymerlinparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(change_url))
    price = scrapy.Field(input_processor=Compose(concat_price), output_processor=TakeFirst())
    params = scrapy.Field(input_processor=Compose(clear_params))
