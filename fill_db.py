from pymongo import MongoClient
#функция подключения к бд
def connect_to_db(db_name):
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    return db
#заполнение коллекции collection_name БД db_name списком items_list
def fill_db(items_list, collection_name,db_name):
    # подключаемся
    db = connect_to_db(db_name)
    # проверяем, есть ли уже такая коллекция, если нет создаем
    if collection_name not in db.collection_names():
        mycollection = db.create_collection(collection_name)
    else:
        mycollection = db.get_collection(collection_name)
    #collection_name.drop({})
    #заполняем
    for item in items_list:
        mycollection.update_one(item, {'$set': item}, upsert=True)
    print('Загружено документов в БД: ', mycollection.find({}).collection.count_documents({}))
    return
#функция удаления бд была нужна для отладки
def drop_db(db_name):
    client = MongoClient('localhost', 27017)
    client.drop_database(db_name)
    db = client[db_name]
    return