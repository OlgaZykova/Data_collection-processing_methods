#1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB
# и реализовать функцию, записывающую собранные вакансии в созданную БД.
#2. Написать функцию, которая производит поиск и выводит на экран вакансии
# с заработной платой больше введённой суммы.
#3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.

from pymongo import MongoClient
from func import fill_vacancies_list, fill_mongodb,find_vacancies
# заполним список вакансий из ранее заполненного файла
vacancies_list = fill_vacancies_list('vacancies.csv')

client = MongoClient ('localhost',27017)
db = client['vacancies']
#в эту коллекцию сложим вакансии
vacancies_info = db.vacancies_info
#так я проверяла количество вакансий, которые хранились до апдейта списка вакансий
print(client ['vacancies'].vacancies_info.find({}).collection.count_documents({}))
#заполним/проапдейтим коллекцию с вакансиями
vacancies_info = fill_mongodb(vacancies_list,vacancies_info)
# посмотрим добавились ли новые вакансии
print(client ['vacancies'].vacancies_info.find({}).collection.count_documents({}))
#теперь будем искать вакансии с зп выше указанной
salary = int(input('Введите зарплату: '))
#и распечатаем список
find_vacancies(salary,vacancies_info)
