# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы) с сайтов Superjob и HH.
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# * Наименование вакансии.
# * Предлагаемую зарплату (отдельно минимальную, максимальную и валюту).
# * Ссылку на саму вакансию.
# * Сайт, откуда собрана вакансия.

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd
# функция конвертации текста с описанием зп в словарь
from funcs import convert_text_to_dict
#инициализируем искомый список вакансий
# каждый элемент списка будет заполнен словарем с элементами название, зарплата (словарь), ссылка на вакансию, сайт
vacancy_list = []
#сюда пользователь введет вакансию
text = input('Введите текст запроса: ')
#Инициализируем номер страницы
i = 0
url = 'http://hh.ru/'
# без изменения user-agent возвращалась 404 ошибка
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64'}
condition = True
# условие выхода из цикла - не нашли на странице ни одной вакансии
while condition:
    params = {'text': text, 'page': i}
    response = requests.get(url+'search/vacancy', params=params, headers=headers)
    dom = bs(response.text, 'html.parser')
# найдем список всех вакансий на странице
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})
    #если список не пуст
    if vacancies:
        for vacancy in vacancies:
            vacancy_data = {}
            vacancy_data['url']=url
            vacancy_name = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
            vacancy_ref = vacancy.find('a')['href']
            vacancy_salary = vacancy.find('span',{'data-qa':'vacancy-serp__vacancy-compensation'})
            #если вообще указана зп
            if vacancy_salary:
                vacancy_data['salary']=convert_text_to_dict(vacancy_salary.getText())
            else:
                vacancy_data['salary']='Не указана'
            vacancy_data['name'] = vacancy_name.getText()
            vacancy_data['ref'] = vacancy_ref
            vacancy_list.append(vacancy_data)
        #сдвиг номера страницы
        i+=1
    else:
        condition=False
# перегрузим результат в датафрейм и сохраним в csv-файл
df = pd.DataFrame(vacancy_list)
df.to_csv('vacancies.csv')
# а так можно проверить вывод датафрейма на экран
if not df.empty:
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)
    print(df)
