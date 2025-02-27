import time
import random as rd

import pandas as pd
import selenium 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

domain = 'https://minecraft-inside.ru'
table = pd.DataFrame(columns=['name', 'download link'])

login = 'MID_SF' # id = loginform-username
password = 'Z_X_C_TblCHKA_TblCHKA_BKB' # id = loginform-password
# button class = btn_primary

options_fire_fox = webdriver.FirefoxOptions()
options_fire_fox.add_argument('Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0')

driver = webdriver.Firefox(options=options_fire_fox)
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

for number_of_page in range(1, 3): # range от 1 до 3 это с первой страницы по вторую спарсить включительно. 
                                   # Оставил две страницы чтобы была пагинация и не нужно было долго ждать 
                                   # я не разобрался как отключить скачивание картинок, 
                                   # так что ждать загрузки сайта приходится долго :(
    time.sleep(3 + rd.random()*(2))
    counter = 0
    driver.get(domain + "/mods/page/" + str(number_of_page))
    elems = driver.find_elements(By.CLASS_NAME, 'post')
    max_counter = len(elems)
    while (counter < max_counter):
        time.sleep(3 + rd.random()*(2)))
        driver.get(domain + "/mods/page/" + str(number_of_page))
        elems = driver.find_elements(By.CLASS_NAME, 'post')
        link = elems[counter].find_element(By.TAG_NAME, 'a').get_attribute('href')
        driver.get(link)
        link2download = driver.find_element(By.CLASS_NAME, "dl__link").text
        name = driver.find_element(By.CLASS_NAME, "box__title").text.split('[')[0]
        table.loc[len(table)] = [name, link2download]
        print(name, link2download)
        counter += 1
table.to_csv('out.csv')
driver.close()
