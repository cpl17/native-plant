
import pandas as pd 

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException,TimeoutException,WebDriverException
from bs4 import BeautifulSoup
import os

import time

from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

PATH = "C:\Program Files (x86)\chromedriver.exe"
DELAY = 2

#Metadata and Source Data
era_pa = pd.read_excel("./Data/PA Wildflower Database.xlsx",sheet_name="ERA_PA")
data = era_pa[["USDA Symbol","Scientific Name","Common Name"]]

#Lists to fill with Names of Matches and URLs
matches_list= []
match_urls_list = []


#Helpers 
def find_matches(list_of_names,data):

    l2 = [x.split(",")[0] for x in list_of_names]
    l2 = sorted(list(set(l2)))

    matches = []

    for name in l2:
        if name in data["Scientific Name"].to_list():
            matches.append(name)

    return matches


############### Scraping ############
driver = webdriver.Chrome(executable_path=PATH,options=chrome_options)

link = "https://midatlanticnatives.com/product-category/bare-root-native-plants/"

driver.get(link)

for i in range(7):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)

element_list = driver.find_elements(By.CSS_SELECTOR,"div h2 a")
list_of_text = [element.text for element in element_list]
list_of_names = [" ".join(x.split(" ")[:2]).strip(",") for x in list_of_text]


with open("MAN_list.txt","w") as f:
    for name in list_of_names:
        print(name)
        f.write(name +"\n")

unique_list = sorted(list(set(list_of_names)))

matches_list = find_matches(unique_list,data)
print(matches_list)

for match_name in matches_list:

    try:
        match_element = driver.find_element(By.PARTIAL_LINK_TEXT,match_name)
        match_element.click()
    except:
        match_urls_list.append("Error")

    time.sleep(2)

    url = driver.current_url

    match_urls_list.append(url)

    driver.back()

    time.sleep(2)


driver.close()

pd.DataFrame({"Scientific Names":matches_list,"URLS":match_urls_list}).to_csv("MAN_Final.csv")




    
