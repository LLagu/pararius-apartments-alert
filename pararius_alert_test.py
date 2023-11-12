from libraries.pararius_alert import *
from libraries.file_management import *

from bs4 import BeautifulSoup
import time
import asyncio

def TestWithRemovedElement():
    
    #Should not find any apartment
    EXPECTED_OUTPUT = 0

    page_source = loadFileContent("test/pageSourceFull.txt")
    soup = BeautifulSoup(page_source, 'html.parser')
    oldRes = soup.find_all("h2", {"class": "listing-search-item__title"})

    page_source = loadFileContent("test/pageSourceTopElemRemoved.txt")
    soup = BeautifulSoup(page_source, 'html.parser')
    currentRes = soup.find_all("h2", {"class": "listing-search-item__title"})

    find_new_apartments(oldRes, currentRes)

    if find_new_apartments(oldRes, currentRes):
        TEST_OUTPUT = 1
    else:
        TEST_OUTPUT = 0

    return TEST_OUTPUT == EXPECTED_OUTPUT


def TestWithNewElement():
    
    #Should find a new apartment
    EXPECTED_OUTPUT = 1

    page_source = loadFileContent("test/pageSourceFull.txt")
    soup = BeautifulSoup(page_source, 'html.parser')
    oldRes = soup.find_all("h2", {"class": "listing-search-item__title"})

    page_source = loadFileContent("test/pageSourceNewElem.txt")
    soup = BeautifulSoup(page_source, 'html.parser')
    currentRes = soup.find_all("h2", {"class": "listing-search-item__title"})

    find_new_apartments(oldRes, currentRes)

    if find_new_apartments(oldRes, currentRes):
        TEST_OUTPUT = 1
    else:
        TEST_OUTPUT = 0

    return TEST_OUTPUT == EXPECTED_OUTPUT

def parametrizedParsePage(p_pageSource1, p_pageSource2):
    loop = asyncio.new_event_loop() 
    asyncio.set_event_loop(loop)

    print("Getting the page source")
    page_source = p_pageSource1
    soup = BeautifulSoup(page_source, 'html.parser')
    res = soup.find_all("h2", {"class": "listing-search-item__title"})

    TEST_i = 0

    #While True loop starts here in the actual function
    current_res = res

    page_source = p_pageSource2
    soup = BeautifulSoup(page_source, 'html.parser')
    res = soup.find_all("h2", {"class": "listing-search-item__title"})

    if res:

        if TEST_i == 0:
            print("Looking for changes. Stand by and wait for a notification")
            TEST_i += 1
        
        new_apartments = find_new_apartments(res, current_res)
        if (not new_apartments):
            time.sleep(1)
        else:
            #send notification
            loop = asyncio.get_event_loop()
            loop.run_until_complete(sendTelegramNotification(new_apartments, "TEST message to the broker"))

            #for logging purposes
            print('Nieuwe aanbieding gedetecteerd')

            time.sleep(1)

def testMain():
    #TEST 1
    print("Test 1: ", TestWithRemovedElement())
    #TEST 2
    print("Test 2: ", TestWithNewElement())


    #
    parametrizedParsePage(loadFileContent("test/pageSourceFull.txt"), loadFileContent("test/pageSourceNewElem.txt"))
testMain()