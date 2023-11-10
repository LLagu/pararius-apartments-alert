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

async def sendTelegramNotification(p_userUrl):
    await telegram_send.send(messages=["Change detected in your search: ", p_userUrl])

def ParsePage(p_userUrl):


    loop = asyncio.new_event_loop() 
    asyncio.set_event_loop(loop)

    print("Getting the page source")
    page_source = GetPageSource(p_userUrl)
    soup = BeautifulSoup(page_source, 'html.parser')
    res = soup.find_all("h2", {"class": "listing-search-item__title"})

    while True:
        current_res = res

        page_source = GetPageSource(p_userUrl)
        soup = BeautifulSoup(page_source, 'html.parser')
        res = soup.find_all("h2", {"class": "listing-search-item__title"})
        highlighted = soup.find_all("span", {"class": "listing-label listing-label--featured"})

        if highlighted:
            comparisonIndex = 1
        else:
            comparisonIndex = 0
        if res:
            print("Looking for changes")
            if (current_res[comparisonIndex] == res[comparisonIndex + 1]):
                time.sleep(25)
            else:
                #send notification
                loop = asyncio.get_event_loop()
                loop.run_until_complete(sendTelegramNotification(p_userUrl))

                #for logging purposes
                mytext = 'Nieuwe aanbieding gedetecteerd'
                print(mytext)
                print(p_userUrl)

                time.sleep(25)
    
