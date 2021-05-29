from lxml import html
from pprint import pprint
import requests
from datetime import datetime,timedelta,time
#функция идет по заданному url и возвращает дом по тексту страницы
def create_dom(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    response = requests.get(url)
    #print(response.url) # тут я проверяла не послал ли меня яндекс к своей странице с капчей
    dom = html.fromstring(response.text)
    return dom
#сбор информации с сайта lenta.ru и записывание их в список news
def collect_from_lenta(news):
    url = 'http://lenta.ru'
    dom = create_dom(url)
    #собираем ссылки на новости с главной страницы из топ-7
    links = dom.xpath("//section[contains(@class,'top-seven')]//div[@class='item']/a/@href")
    # для каждой новости заходим внутрь, формируем дом и вытаскиваем информацию
    for link in links:
        news_item = {}
        news_item['link'] = url + link
        dom = create_dom(news_item['link'])
        dt= dom.xpath("//div[contains(@class,'topic__info')]/time/@datetime")[0]
        # здесь конвертирую дату в строку формата "Y-m-d H:m:s"
        dt = str(dt)
        dt = dt.replace('T',' ')
        dt = dt.split('+')[0]

        news_item['pub_datetime'] =dt
        news_item['topic'] = dom.xpath("//div[contains(@class,'topic__header')]/h1[@class = 'b-topic__title']/text()")[
            0]
        #заменяем неделимые пробелы на обычные
        news_item['topic'] = news_item['topic'].replace('\xa0', ' ')
        news_item['sourse'] = 'lenta.ru'
        news.append(news_item)
    return
#функция конвертирует строку с датой-временем из яндекса в строку вида "Y-m-d H:m:s"
# используется для новостей из яндекса
def convert_to_date(text):
    now = datetime.now().date()
    tmp = text.split()
    # "вчерв в время"
    if len(tmp) == 3:
        dmy = now-timedelta(days=1)
    #"время" (сегодня)
    elif len(tmp)==1:
        dmy = now
    #"25 мая в время"
    else:
        day = int(tmp[0])
        m_dict = {'января':1,'февраля':2,'марта':3,'апреля':4,
                  'мая':5,'июня':6,'июля': 7,'августа':8,
                  'сентября':9,'октября':10,'ноября':11,'декабря':12}
        mounth = m_dict[tmp[1]]
        year = now.year
        dmy = datetime(year,mounth,day)
    new_date = dmy.strftime('%Y-%m-%d')
    hour_min = tmp[-1]+':00'
    new_date =new_date + ' '+ hour_min
    return new_date
#сбор новостей с сайта yandex.news
def collect_from_yandex(news):
    #начинаем со стартовой страницы новостей
    url = 'https://yandex.ru/news/'
    dom = create_dom(url)
    #ищем ссылку на страницу с желаемой рубрикой, у меня Экология
    url2 = dom.xpath("//span[text()='Экология']/../@href")[0]
    dom = create_dom(url2)

## В какой-то момент яндекс стал принимать меня за робота и на все мои запросы редиректил меня на
## страницу с капчей, пришлось скачать себе код страницы и парсить его из файла
## ЗАкомментированным ниже кодом формировала dom в этом случае
## Раскомментить в случае необходимости, файл .txt приложу!

   # with open('ya_text.txt','r',encoding='utf-8') as infile:
    #    text=infile.read()
    #dom = html.fromstring(text)

    #собираем массив ссылок, названий статей, источников, дат публикаций
    links = dom.xpath("//article/a/@href | //article/div[@class='mg-card__inner']/a/@href")
    titles = dom.xpath("//article//h2[@class = 'mg-card__title']/text()")
    sources = dom.xpath("//a[@aria-label]/text()")
    pub_dates = dom.xpath("//span[@class = 'mg-card-source__time']/text()")
    #формируем наш список новостей
    for link,title,source,pub_date in zip(links,titles,sources,pub_dates):
        news_item = {}
        news_item['link'] = link
        news_item['pub_datetime'] = convert_to_date(pub_date)
        news_item['topic'] = title
        news_item['source'] = source
        news.append(news_item)
    return