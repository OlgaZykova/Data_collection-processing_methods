from pymongo import MongoClient
from func import fill_vacancies_list, fill_mongodb,find_vacancies
# заполним БД новостями - ранее загруженные добавлены не будут
def fill_db(news_list):
    client = MongoClient ('localhost',27017)
    db = client['news']
    #в эту коллекцию сложим новости
    news_info = db.news_info
    #news_info.drop({})
    for news_item in news_list:
        news_info.update_one(news_item,{'$set':news_item},upsert=True)
    print('Загружено новостей в БД: ', news_info.find({}).collection.count_documents({}))
    return
