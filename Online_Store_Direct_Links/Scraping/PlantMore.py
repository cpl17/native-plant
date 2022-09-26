import pandas as pd 

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException,TimeoutException,WebDriverException
from bs4 import BeautifulSoup
import os

import time

PATH = "C:\Program Files (x86)\chromedriver.exe"
DELAY = 2


#Metadata and Source Data
era_pa = pd.read_excel("./Data/PA Wildflower Database.xlsx",sheet_name="ERA_PA")
data = era_pa[["USDA Symbol","Scientific Name","Common Name"]]

#Dictionary to fill with Names of Matches and URLs
names_url = {}
matches_list= []
match_urls_list = []


#Helpers 
def wait_until_page_load(_):

    if int(driver.find_element(By.CLASS_NAME,"wsite-selected").text) != (_ +2):
        time.sleep(5)
        wait_until_page_load(_)


def find_matches(list_of_names,data):

    l2 = [x.split("'")[0].split("(")[0].strip("\n").rstrip() for x in list_of_names]
    l2 = sorted(list(set(l2)))

    matches = []

    for name in l2:
        if name in data["Scientific Name"].to_list():
            matches.append(name)
    
    return matches


######### Scraping #########

# Open Initial Page
driver = webdriver.Chrome(executable_path=PATH)

link = "https://www.plantmorenatives.com/store/c26/native_perennial_plant_store#/"

driver.get(link)

#Wait for pop-up and close. It does not return 
time.sleep(10)
pop_up = driver.find_element(By.XPATH,"//*[@id='leadform-popup-close-576d6d25-a6a2-40cb-ab77-1205e75d2f2e']")
pop_up.click()


# Get names and urls from first page
name_elements = driver.find_elements(By.CLASS_NAME,"wsite-com-link-text")
list_of_names_from_page = [element.text for element in name_elements]

matches_from_page = find_matches(list_of_names_from_page,data)
matches_list.extend(matches_from_page)

for match_name in matches_from_page:

    match_element = driver.find_element(By.PARTIAL_LINK_TEXT,match_name)
    match_element.click()

    time.sleep(2)

    url = driver.current_url

    match_urls_list.append(url)

    driver.back()

    time.sleep(2)


print(match_urls_list)
print(matches_list)

# Get names and urls from the remaining pages 

xpaths_for_pages = [f"//*[@id='wsite-com-category-product-group-pagelist']/a[{page_number}]" for page_number in range(3,8)]
for i,path in enumerate(xpaths_for_pages):

    print(match_urls_list)
    print(matches_list)

    page_element = driver.find_element(By.XPATH,path)
    page_element.click()

    wait_until_page_load(i)

    # current_page_number = int(driver.find_element(By.CLASS_NAME,"wsite-selected").text)
    # print(current_page_number)

    name_elements = driver.find_elements(By.CLASS_NAME,"wsite-com-link-text")
    list_of_names_from_page = [element.text for element in name_elements]
    
    matches_from_page = find_matches(list_of_names_from_page,data)
    matches_list.extend(matches_from_page)


    for match_name in matches_from_page:

        match_element = driver.find_element(By.PARTIAL_LINK_TEXT,match_name)
        match_element.click()

            
        time.sleep(2)

        url = driver.current_url

        match_urls_list.append(url)

        driver.back()

        time.sleep(2)

driver.close()


pd.DataFrame({"Scientific Names":matches_list,"URLS":match_urls_list}).to_csv("Final.csv")

