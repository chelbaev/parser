import time
import random as rd

import pandas as pd
import selenium 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

domain = 'https://minecraft-inside.ru'
table = pd.DataFrame(columns=['name', 'download link'])

login = input("Введите логин, для входа на сайт: ")
password = input('Введите пароль, для входа на сайт: ') # id = loginform-password
# button class = btn_primary

start = int(input('с какой страницы начать? :'))
end = int(input('на какой странице закончить? (включительно):'))

while (start < 0 or end < start or end > 1453):
    print('вы ввели первую или последнюю страницу не правильно, повторите попытку')
    start = int(input('с какой страницы начать? :'))
    end = int(input('на какой странице закончить? (включительно):'))

options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0')
options_chrome.add_argument('--blink-settings=imagesEnabled=false')
options_chrome.add_argument('--disable-extensions')
options_chrome.add_argument('--disable-popup-blocking')
options_chrome.add_argument('--disable-notifications')


driver = webdriver.Chrome(options=options_chrome)
try:
    driver.get('https://minecraft-inside.ru/login/')
    login_input = driver.find_element(By.ID, "loginform-username")
    password_input = driver.find_element(By.ID, "loginform-password")
    button_send = driver.find_element(By.CLASS_NAME, 'btn_primary')
    login_input.clear()
    password_input.clear()
    login_input.send_keys(login)
    time.sleep(3 + rd.random()*(2))    
    password_input.send_keys(password)
    time.sleep(3 + rd.random()*(2))
    button_send.click()

except Exception as ex:
    print(ex)

for number_of_page in range(start, end + 1): 
    time.sleep(3 + rd.random()*(2))
    counter = 0
    driver.get(domain + "/mods/page/" + str(number_of_page))
    elems = driver.find_elements(By.CLASS_NAME, 'post')
    links = list()
    for elem in elems:
        links.append(elem.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    max_counter = len(elems)
    for link in links:
        time.sleep(3 + rd.random()*(2))
        driver.get(link)
        link2download = driver.find_element(By.CLASS_NAME, "dl__link").text
        name = driver.find_element(By.CLASS_NAME, "box__title").text.split('[')[0]
        table.loc[len(table)] = [name, link2download]
        counter += 1
table.to_csv('out.csv')
driver.close()
