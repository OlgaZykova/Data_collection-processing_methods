
import requests
import json

#запросим ввод имени интересующего пользователя
username = input('Введите имя пользователя: ')

#сформируем корректную ссылку
url = 'https://api.github.com/users/'+username+'/repos'

#запросим список репозиториев для пользователя
response = requests.get(url)
j_data = response.json()
#запишем результат в файл
with open('data.json', 'w') as outfile:
    json.dump(j_data, outfile)
