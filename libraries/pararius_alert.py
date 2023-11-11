from libraries.setup import *
from libraries.install_dependencies import *


from bs4 import BeautifulSoup
import time
import telegram_send
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import warnings
import asyncio

def GetPageSource(p_userUrl):
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)
        driver = webdriver.Firefox(options=options)
    driver.get(p_userUrl)
    #TODO: eventually replace the sleep with a control that lets the function proceed once
    # the page is fully loaded
    time.sleep(5)
    pageSource = driver.page_source
    driver.close()
    return pageSource

async def sendTelegramNotification(p_userUrl, p_messageToTheBroker):
    if p_messageToTheBroker != "":
        await telegram_send.send(messages=["Change detected in your search: ", p_userUrl])
    else:
        await telegram_send.send(messages=["Change detected in your search: ", p_userUrl, p_messageToTheBroker])

def find_new_apartments(old_vacancies, updated_vacancies):
    # Exclude the last element
    if updated_vacancies and updated_vacancies[-1] not in old_vacancies:
        updated_vacancies = updated_vacancies[:-1]

    new_apartments = set(updated_vacancies) - set(old_vacancies)
    return new_apartments

def ParsePage(p_userUrl, p_messageToTheBroker):


    loop = asyncio.new_event_loop() 
    asyncio.set_event_loop(loop)

    print("Getting the page source")
    page_source = GetPageSource(p_userUrl)
    soup = BeautifulSoup(page_source, 'html.parser')
    res = soup.find_all("h2", {"class": "listing-search-item__title"})

    TEST_i = 0

    while True:
        current_res = res

        page_source = GetPageSource(p_userUrl)
        soup = BeautifulSoup(page_source, 'html.parser')
        res = soup.find_all("h2", {"class": "listing-search-item__title"})

        if res:
  
            if TEST_i == 0:
                print("Looking for changes. Stand by and wait for a notification")
                TEST_i += 1
            
            if (not find_new_apartments(res, current_res)):
                time.sleep(25)
            else:
                #send notification
                loop = asyncio.get_event_loop()
                loop.run_until_complete(sendTelegramNotification(p_userUrl, p_messageToTheBroker))

                #for logging purposes
                print('Nieuwe aanbieding gedetecteerd')
                print(p_userUrl)

                time.sleep(25)
    
