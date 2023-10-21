from libraries.setup import *
from libraries.install_dependencies import *
import libraries.constants as const

###USER SETUP
userOptions = []
GetUserOptions(userOptions)
if(userOptions[const.optionIndexFirstSetup]):
    InstallDependencies()
    print('////////////////////////////////////////////////////////////////\n////////////////////////////////////////////////////////////////')
    print('Dependencies installed')
    print('////////////////////////////////////////////////////////////////\n////////////////////////////////////////////////////////////////')
if(userOptions[const.optionIndexNewNumber]):
    print('To setup the new number follow the next steps:')
    print('1. Go to https://telegram.me/BotFather and send the message "/newbot" to the chat')
    print('2. Open the command prompt and type "telegram-send --configure"')
    print('If the system does not recognise the command add your Python\\Script to PATH')
    print('3. Continue here once the telegram configuration is successfully completed')
    input('Press any key to continue')
url = userOptions[const.optionIndexURL]
print('Parsing started. You\'ll receive a notification when a change is detected.')
###

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

def ParsePage():
    page_source = GetPageSource(url)
    soup = BeautifulSoup(page_source, 'html.parser')
    res = soup.find_all("h2", {"class": "listing-search-item__title"})

    while True:
        current_res = res

        page_source = GetPageSource(url)
        soup = BeautifulSoup(page_source, 'html.parser')
        res = soup.find_all("h2", {"class": "listing-search-item__title"})
        highlighted = soup.find_all("span", {"class": "listing-label listing-label--featured"})

        if highlighted:
            comparisonIndex = 1
        else:
            comparisonIndex = 1
        if res:
            if (current_res[comparisonIndex] == res[comparisonIndex]):
                time.sleep(25)
            else:
                telegram_send.send(messages=["Change detected in your search: ", url])
                mytext = 'Nieuwe aanbieding gedetecteerd'
                print(mytext)
                print(url)

                time.sleep(25)