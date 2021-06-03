#1) Написать программу, которая собирает входящие письма из своего
# или тестового почтового ящика и сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма полный)

from funcs import authorization,get_info_from_mail
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from fill_db import fill_db,drop_db
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://mail.ru')
#читаем из файла авторизационные данные
authorization('authorization_info.txt',driver)
# ожидаем загрузки страницы с письмами по кликабельности кнопки "написать письмо"
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@title = 'Написать письмо']")))
#список ссылок на письма, которые будем собирать из списка писем
mail_links = []
actions = ActionChains(driver)

#у меня работает только одна прокрутка, поэтому использовать while true бесполезно
for i in range(1,5):
    mail_list = driver.find_elements_by_xpath("//div[contains(@class,'dataset__items')]/a[@href]")
    for mail in mail_list:
        mail_link = mail.get_attribute('href')
        mail_links.append(mail_link)
    #смещаемся на последнее подгруженное письмо - оно в конце страницы и дальше письма не грузятся
    actions.move_to_element(mail_list[-1]).perform()
    # подождем, пока список писем подтянется
    time.sleep(3)
    #выкинем дубли
    mail_links = list(set(mail_links))
#тут будет список для загрузки в бд
mails_info = []
for mail_link in mail_links:
    mail_info = get_info_from_mail(mail_link, driver)
    mails_info.append(mail_info)
#заполняем бд
#drop_db('mails')
fill_db(mails_info,'mails','mail_data')
driver.close()
