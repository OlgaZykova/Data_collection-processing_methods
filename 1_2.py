# Здесь описана последовательность действий, которую я выполнила частично вручную,
# частично с помощью этого кода
# 1. Залогинилась в браузере в свой аккаунт vk
# 2. Создала Standalone-приложение на вкладке "Мои приложения", скопировала id созданного приложения.
# В настройках приложения установила, что оно активно.
# 3. Далее необходимо получить токен для авторизации. Это делается с помощью нижие приведенного кода
# импорт библиотек
from pprint import pprint
import requests
import json
#чтобы не формировать корректную ссылку для получения токена вручную сделаю это запросом get
# в качестве client_id указываю id ранее созданного приложения
# остальные параметры заполняю в соответствии с описанием авторизации
params = {
        'client_id':'7856582',
       'redirect_uri':'https://oauth.vk.com/blank.html',
        'display':'page',
        'scope':'groups',
        'response_type':'token',
        'v':'5.130',
        'revoke':'1'}
url='https://oauth.vk.com/authorize'
response=requests.get(url,params)

#4. Отсюда получаю корректно сформированную ссылку и ввожу ее вручную в браузер
print(response.url)
# В качестве ответа в адресной строке браузера получаю строку, содержащую токен
# Вот эту https://oauth.vk.com/blank.html#access_token=fe6c18421ca11036fbdf12fdb88497584ce8a60c84afddf4b0e8012aa2182fa5ae93b260bce3ddb9dd097&expires_in=86400&user_id=638951

# 5. Вызываю метод получения списка групп пользователя, вручную подставив user_id (cвой id) и полученный ранее токен
url='https://api.vk.com/method/groups.get?user_id=638951&access_token=fe6c18421ca11036fbdf12fdb88497584ce8a60c84afddf4b0e8012aa2182fa5ae93b260bce3ddb9dd097&v=5.130'

response=requests.get(url)

# Сохраняю ответ от API в json файл
with open('olyas_communities.json', 'w') as outfile:
    json.dump(response.json(), outfile)