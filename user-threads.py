import time

import requests
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telebot

account = ["login", "password"]
check = "https://forum.arizona-rp.com/search/"

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(options=options)

driver.get("https://forum.arizona-rp.com/")


def login_to_acc(cred):
    driver.get("https://forum.arizona-rp.com/")

    login_form = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[text()="Вход"]')))
    login_form.click()

    username = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@name="login"]')))
    password = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@name="password"]')))
    username.send_keys(cred[0])
    password.send_keys(cred[1])
    password.submit()


def get_user_messages(link):
    driver.get(link + "#recent-content")
    posts = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="top"]/div[3]/div/div/div/div/div/ul/li[2]/div/div/div/span/a')))
    posts.click()
    time.sleep(4)
    input("start?")
    print("start parsing..")
    links = []
    while 1:
        messages = driver.find_elements_by_xpath("/html/body/div[2]/div/div[4]/div/div[2]/div/div/div/div/div[1]/ol/li")
        for message in messages:
            message_link = message.find_elements_by_tag_name("a")[1]
            print(message_link.get_attribute('href'))
            links.append(message_link.get_attribute('href'))

        try:
            next_page = driver.find_element_by_xpath("//a[text()='Вперёд']")
            next_page.click()
        except:
            break
    return links


def find_by_search(author, by_link=False):
    if not by_link:
        driver.get("https://forum.arizona-rp.com/search/")
        users = WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located((By.NAME, 'c[users]')))[0]
        users.send_keys(author)
        users.submit()
    else:
        driver.get(author)
    time.sleep(5)
    links = []
    while 1:
        messages = driver.find_elements_by_xpath("/html/body/div[2]/div/div[4]/div/div[2]/div/div/div/div/div[1]/ol/li")
        if messages is None:
            messages = driver.find_elements_by_xpath("/html/body/div[2]/div/div[4]/div/div[2]/div/div/div/div/div[2]/ol/li")

        for message in messages:
            message_link = message.find_elements_by_tag_name("a")[1]
            print(message_link.get_attribute('href'))
            links.append(message_link.get_attribute('href'))

        try:
            next_page = driver.find_element_by_xpath("//a[text()='Вперёд']")
            next_page.click()
        except:
            break
    return links


def make_reaction(link, uid):
    reacted = False
    if "post-" in link:
        print("[+] Ставлю реакцию на " + link)
        link = link.split("post-")[1].replace("/", "")
        try:
            driver.get("https://forum.arizona-rp.com/posts/" + link + "/react?reaction_id=" + str(uid))
            react = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="top"]/div[4]/div/div/div/div/div/form/div/dl/dd/div/div[2]/button')))
            react.click()
            reacted = True
        except:
            print("[-] Произошла ошибка при установке реакции")
    else:
        if "https://forum.arizona-rp.com/threads/" in link:
            print("[+] Ставлю реакцию на " + link)
            try:
                driver.get(link)
                WebDriverWait(driver, 5).until(EC.visibility_of_any_elements_located((By.TAG_NAME, "article")))
                soup = BeautifulSoup(driver.page_source, "lxml")
                for post in soup.findAll('article', {'class': 'message'}):
                    hrefs = post.findAll('a')
                    for a in hrefs:
                        if "/post-" in a['href']:
                            number = a['href'].split("post-")[1].replace("/", "")
                            print("[~] Найден номер поста " + str(number))
                            driver.get("https://forum.arizona-rp.com/posts/" + number + "/react?reaction_id=" + str(uid))
                            react = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                                (By.XPATH, '//*[@id="top"]/div[4]/div/div/div/div/div/form/div/dl/dd/div/div[2]/button')))
                            react.click()
                            reacted = True
                            break
                        if reacted:
                            break
                    if reacted:
                        break
            except:
                print("[-] Произошла ошибка при установке реакции")
    time.sleep(1)
    return reacted


def dis_reaction():
    #links = get_user_messages(check)

    with open('clowns.txt') as f:
        lines = f.readlines()

    s = input("Всего найдено {} постов. Начать anal дебош?".format(str(len(lines))))

    results = {'good': 0, 'bad': 0}
    for link1 in lines:
        if make_reaction(link1.replace("\n", ""), 6):
            results['good'] += 1
        else:
            results['bad'] += 1

    print("Задача завершена\n{} - Good\n{} - Bad".format(results['good'], results['bad']))


login_to_acc(account)
time.sleep(3)
dis_reaction()
#find_by_search("https://forum.arizona-rp.com/search/4926174/", True)