from libraries.setup import *
from libraries.install_dependencies import *
import libraries.constants as const


from bs4 import BeautifulSoup
import time
from gtts import gTTS
import os
import telegram_send
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import warnings

def GetPageSource(p_userURL):
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)
        driver = webdriver.Firefox(options=options)
    driver.get(p_userURL)
    time.sleep(5)
    pageSource = driver.page_source
    driver.close()
    return pageSource

def ParsePage(p_userURL):
    page_source = GetPageSource(p_userURL)
    soup = BeautifulSoup(page_source, 'html.parser')
    res = soup.find_all("h2", {"class": "listing-search-item__title"})

    while True:
        current_res = res

        page_source = GetPageSource(p_userURL)
        soup = BeautifulSoup(page_source, 'html.parser')
        res = soup.find_all("h2", {"class": "listing-search-item__title"})
        highlighted = soup.find_all("span", {"class": "listing-label listing-label--featured"})

        if highlighted:
            comparisonIndex = 1
        else:
            comparisonIndex = 0
        if res:
            if (current_res[comparisonIndex] == res[comparisonIndex]):
                time.sleep(25)
            else:
                telegram_send.send(messages=["Change detected in your search: ", p_userURL])
                mytext = 'Nieuwe aanbieding gedetecteerd'
                print(mytext)
                print(p_userURL)

                time.sleep(25)