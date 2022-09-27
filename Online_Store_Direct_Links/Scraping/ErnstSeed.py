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
scientific_names = data["Scientific Name"].to_list()

#Lists to fill with Names of Matches and URLs
matches_list= []
match_urls_list = []

#Open Species Page
driver = webdriver.Chrome(executable_path=PATH)
home_page = "https://www.ernstseed.com/products/individual-species/"
driver.get(home_page)


#Get Link Elements, Name Elements and write all the available species to a text file 
link_elements = driver.find_elements(By.CSS_SELECTOR,"div h3 strong a")
name_elements = driver.find_elements(By.CSS_SELECTOR,"div h3 strong a i")
names = [name.text for name in name_elements]

with open("ErnstSeed.txt","w") as f:
    for name in names:
        f.write(name + "\n")


#Find Matches. All relevant links have a child italize tag that holds the name 
for link in link_elements:
    try:
        name_element = link.find_element(By.TAG_NAME,"i")
        name = name_element.text.split(',')[0] 
        print(name)
    except:
        continue

    if name in scientific_names:
        matches_list.append(name)
        match_urls_list.append(link.get_attribute("href"))




data = pd.DataFrame({"Scientific Names":matches_list,"URLS":match_urls_list})
data = data.drop_duplicates(subset="Scientific Names",keep='first')
data.to_csv("ES_Final.csv")




