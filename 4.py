# Написать приложение, которое собирает основные новости с сайтов
# news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath.
# Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные данные в БД

from collect_info_funcs import collect_from_lenta,collect_from_yandex
from fill_db import fill_db
news = []
#сбор новостей
collect_from_lenta(news)
collect_from_yandex(news)
print('Распечатаем список найденных новостей: ')
for i,news_item in zip(range(1,len(news)+1),news):
    print(i, '  ',news_item, '\n')
#заполнение бд
fill_db(news)