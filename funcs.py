from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
#читаем из файла информацию для авторизации
def read_authorization_info(filename):
    with open(filename, 'r') as f:
        login = f.readline().split(':')[1].replace('\n','')
        password = f.readline().split(':')[1]
    return [login, password]
#авторизируемся в почту
def authorization(filename,driver):
    # читаем из файла авторизационные данные
    login = read_authorization_info(filename)[0]
    password = read_authorization_info(filename)[1]
    # ждем прогруза страницы
    time.sleep(3)
    element = driver.find_element_by_class_name('email-input')
    element.send_keys(login)
    element = driver.find_element_by_xpath("//button[@data-testid='enter-password']")
    element.send_keys(Keys.ENTER)
    element = driver.find_element_by_class_name('password-input')
    element.send_keys(password)
    element.send_keys(Keys.ENTER)
    return
#собираем информацию из одного письма
def get_info_from_mail(mail_link,driver):
    #открываем ссылку с письмом
    driver.get(mail_link)
    mail_info = {}
    #ждем, пока страница с пиьмом загрузится по кликабельности ссылки "Написать письмо"
    #текст письма не собираю!! Не поняла как это сделать в нормальном виде, текст всех писем оформлен как-то очень по-разному
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@title = 'Написать письмо']")))
    mail_info['author'] = driver.find_element_by_xpath("//div[@class='letter__author']/span[contains(@class,'letter-contact')]").text
    mail_info['date'] = driver.find_element_by_xpath("//div[@class='letter__date']").text
    mail_info['topic'] = driver.find_element_by_xpath("//h2[@class='thread__subject']").text
    return mail_info
