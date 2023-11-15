from libraries.install_dependencies import *

from bs4 import BeautifulSoup
import time
import telegram_send
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import warnings
import asyncio

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def GetPageSource(p_userUrl):
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        driver = webdriver.Firefox(options=options)
    
    try:
        # Set a longer timeout for page navigation (e.g., 60 seconds)
        driver.set_page_load_timeout(60)
        driver.get(p_userUrl)

        # Wait for the presence of an element with a specific class (adjust as needed)
        # WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'listing-search-item__title')))
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'listing-search-item__title')))
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//body[not(@class="loading")]')))

        pageSource = driver.page_source
    finally:
        driver.quit()
    
    return pageSource


async def sendTelegramNotification(p_apartmentsList, p_messageToTheBroker):
        for property in p_apartmentsList:
            #By using the *property syntax, you are unpacking the elements of the property list, and they will be passed as separate arguments to the send function.
            await telegram_send.send(messages=[("New property: ", *property)])
        await telegram_send.send(messages=[(p_messageToTheBroker)])

def find_new_apartments(old_vacancies, updated_vacancies):
    ret = []
    # Exclude the last element
    if updated_vacancies and updated_vacancies[-1] not in old_vacancies:
        updated_vacancies = updated_vacancies[:-1]

    print("------------------------DEBUG--------------------------")
    print("old = ", old_vacancies[0].find('a').get_text(strip=True))
    print("new = ", updated_vacancies[0].find('a').get_text(strip=True))
    print("-------------------------------------------------------")
    new_apartments = set(updated_vacancies) - set(old_vacancies)
    
    for property in new_apartments:
        # print("property = ", property)
        name = property.find('a').get_text(strip=True)
        href = property.find('a')['href']
        ret.append((name, "https://www.pararius.nl" + href))
    return ret

def ParsePage(p_userUrl, p_messageToTheBroker):
    loop = asyncio.new_event_loop() 
    asyncio.set_event_loop(loop)

    print("Getting the page source")
    page_source = GetPageSource(p_userUrl)
    soup = BeautifulSoup(page_source, 'html.parser')
    old_res = soup.find_all("h2", {"class": "listing-search-item__title"})

    TEST_i = 0
    DEBUG_state_index = 0

    while True:
        

        page_source = GetPageSource(p_userUrl)
        soup = BeautifulSoup(page_source, 'html.parser')
        # res = soup.find_all("h2", {"class": "listing-search-item__title"})
        current_res = soup.find_all("h2", {"class": "listing-search-item__title"})

        if current_res:
            # print("Still running. Check #", DEBUG_state_index)
            # DEBUG_state_index += 1
            if TEST_i == 0:
                print("Looking for changes. Stand by and wait for a notification")
                TEST_i += 1
            
            new_apartments = find_new_apartments(old_res, current_res)
            if (not new_apartments):
                # loop = asyncio.get_event_loop()
                # loop.run_until_complete(sendTelegramNotification(["test1", "no new partments"], p_messageToTheBroker))
                old_res = current_res
                time.sleep(25)
            else:
                #send notification
                loop = asyncio.get_event_loop()
                loop.run_until_complete(sendTelegramNotification(new_apartments, p_messageToTheBroker))

                #for logging purposes
                print('Nieuwe aanbieding gedetecteerd')
                print(p_userUrl)

                old_res = current_res
                time.sleep(25)