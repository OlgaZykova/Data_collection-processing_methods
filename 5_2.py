#2) Написать программу, которая собирает «Новинки» с сайта техники mvideo
# и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from fill_db import fill_db
import time
import json


chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://mvideo.ru')
#у меня сайт загружался долго, поэтому ждем аж 5 секунд
time.sleep(5)
#находим блок с новинками - не стала сильно заморачиваться и просто по номеру в списке его нахожу
# не очень конечно надежно
element = driver.find_elements_by_xpath("//div[@class='accessories-carousel-wrapper ']")[1]
actions = ActionChains(driver)
# идем к блоку с новинками на экране - чтобы видно было
actions.move_to_element(element).perform()
# находим кнопку тыкания вправо
element = driver.find_element_by_xpath("//h2[contains(text(),'Новинки')][1]/../../..//a[contains(@class,'next-btn')]")
goods_list = []
# условие выхода из цикла - не находим в рамках итерации ни одного элемента, которого нет в списке
exit_condition = False
while True:
    include_new = False
    if exit_condition:
        break
    #клик на стрелку вправо
    actions.move_to_element(element).click(element).perform()
    #Находим товары
    goods = driver.find_elements_by_xpath("//h2[contains(text(),'Новинки')][1]/../../..//li[@class = 'gallery-list-item']//h3/a")
    for good in goods:
        good_info = good.get_attribute('data-product-info')
        if good_info not in goods_list:
            goods_list.append(good_info)
            #найден новый элемент!
            include_new = True
        else:
            exit_condition = True*(not include_new)

goods_list_json = []
# конвертируем в json и заполняем список из json'ов
for good in goods_list:
    goods_json = json.loads(good)
    goods_list_json.append(goods_json)
driver.close()
#кладем в бд
fill_db(goods_list_json,'goods','goods_data')
