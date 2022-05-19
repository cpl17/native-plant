from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from lxml.etree import ParserError
import pandas as pd
import itertools
import numpy as np
import json 



# Global Constansts
PATH = "C:\Program Files (x86)\chromedriver.exe"
BASE_URL = "http://en.wikipedia.org/wiki/"
HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Chrome/87.0.4280.141"
}
DELAY = 10

driver = webdriver.Chrome(executable_path=PATH)




#Get List of names 

df = pd.read_csv(r"C:\Users\CPL17\OneDrive\Documents\Code\On Git\Other\Plants_Final\ERA_PA.csv")

list_of_names = df["Scientific Name"].to_list()
full_dict = dict(zip(list_of_names,[""]*len(list_of_names)))

for name in list_of_names:

    driver.get(BASE_URL + name)

    try:
        WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".infobox.biota")))

    except TimeoutException:
        full_dict.update({name:"No Article"})
        continue

    #Get DF

    full_table_element = driver.find_element_by_class_name("mw-parser-output")
    df_list = pd.read_html(full_table_element.get_attribute("innerHTML"))
    classification_table = df_list[0]


    #Reindex using keys; Set Column Name
    classification_table.set_index(classification_table.columns[0],inplace=True)
    classification_table.columns = [name]


    
    classification_table.index= classification_table.index.astype(str).str.strip(":")
    classification_table = classification_table[classification_table.index.isin(["Kingdom","Order","Family","Clade","Genus","Species","(unranked)"])]

    
    # classification_table[plant_name] = classification_table[plant_name].apply(lambda x: x.replace(u'\xa0', u' ') if not isinstance(x,float) else x )
    # classification_table[plant_name] = classification_table[plant_name].apply(lambda x: str(x) )


    #Create Unique index for Clade Levels
    i = 0
    new_index = []
    for index_value in classification_table.index:
        if index_value == "Clade":
            new_index.append(index_value + str(i))
            i+=1
        else:
            new_index.append(index_value)
    classification_table.index = pd.Index(new_index)




    #Convert to dict; update full dict
    plant_dict = classification_table.to_dict()
    full_dict.update(plant_dict)



with open("plant_classification.json","w") as f:
    json.dump(full_dict,f, indent = 6)




# driver.close()