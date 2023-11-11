from libraries.pararius_alert import *
from libraries.file_management import *

def TestWithRemovedElement():
    
    #Should not find any apartment
    EXPECTED_OUTPUT = 0

    page_source = loadFileContent("pageSourceFull.txt")
    soup = BeautifulSoup(page_source, 'html.parser')
    oldRes = soup.find_all("h2", {"class": "listing-search-item__title"})

    page_source = loadFileContent("pageSourceTopElemRemoved.txt")
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

    page_source = loadFileContent("pageSourceFull.txt")
    soup = BeautifulSoup(page_source, 'html.parser')
    oldRes = soup.find_all("h2", {"class": "listing-search-item__title"})

    page_source = loadFileContent("pageSourceNewElem.txt")
    soup = BeautifulSoup(page_source, 'html.parser')
    currentRes = soup.find_all("h2", {"class": "listing-search-item__title"})

    find_new_apartments(oldRes, currentRes)

    if find_new_apartments(oldRes, currentRes):
        TEST_OUTPUT = 1
    else:
        TEST_OUTPUT = 0

    return TEST_OUTPUT == EXPECTED_OUTPUT


def testMain():
    #TEST 1
    print("Test 1: ", TestWithRemovedElement())
    #TEST 2
    print("Test 2: ", TestWithNewElement())

testMain()