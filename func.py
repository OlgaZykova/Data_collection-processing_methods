import csv
#считать из файла список вакансий
def fill_vacancies_list(file):
    # список вакансий
    vacancies = []
    # считываем список вакансий в список из csv-файла
    with open(file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            vacancies.append(row)
    return vacancies
#найти вакансии с зп выше salary из коллекции vacancies_info mongodb
def find_vacancies(salary,vacancies_info):
    # Условия - зп_от или зп_до больще salary и валюта - русские рубли
    greater_salary_list = vacancies_info.find({'$and':[{'$or': [{'salary_from': {'$gte': salary}}, {'salary_to': {'$gte': salary}}]},{'salary_cur':{'$eq':'руб.'}}]})
    for i,vacancy in zip(range(1, greater_salary_list.collection.count_documents({})+1),greater_salary_list):
        print(f'№{i}: {vacancy}')
    return
# заполнение/апдейт коллекции вакансий на основании нового списка вакансий
def fill_mongodb(vacancies_list,vacancies_info):

    for vacancy in vacancies_list:
        if vacancy['salary_from']:
            vacancy['salary_from'] = float(vacancy['salary_from'])
        if vacancy['salary_to']:
            vacancy['salary_to'] = float(vacancy['salary_to'])
        #будем апдейтить, если такая вакансия уже есть, если нет - то добавлять
        vacancies_info.update_one(vacancy,{'$set':vacancy},upsert=True)
    return vacancies_info
