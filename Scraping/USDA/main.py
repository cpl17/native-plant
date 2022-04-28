from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from lxml.etree import ParserError
import pandas as pd
import itertools
import numpy as np


PATH = "C:\Program Files (x86)\chromedriver.exe"
URL = "https://plants.usda.gov/home/plantProfile?symbol="
DELAY = 3

#Open Page 
driver = webdriver.Chrome(executable_path=PATH)

symbols = pd.read_csv("symbols.csv").squeeze().to_list()
first_symbol = symbols[0]
plant_dict = {}
list_of_indexes = []

skipped_symbols = []

for symbol in symbols:
    
    full_url = URL + symbol

    
    driver.get(full_url)

    #Wait for Charateristics tab to come up and click on it
    try:
        WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.LINK_TEXT, "Characteristics")))
    except TimeoutException:

        skipped_symbols.append(symbol)
        continue
        
        
    characteristics_tab_element = driver.find_element_by_link_text("Characteristics")
    characteristics_tab_element.click()

    #Grab the Characteristcs section html 
    WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    characteristics_table_element = driver.find_element_by_id("characteristics")
    html = characteristics_table_element.get_attribute("innerHTML")

    #Covert table to df, grab index column using index for first df, append symbol:list of data to
    #the plant_dict
    try:
        table_df = pd.read_html(html)
    except ParserError:
        skipped_symbols.append(symbol)
        continue



    #Create and store and index from the available plant characteristics
    index = table_df[0].iloc[:,0]
    list_of_indexes.append(index)

    #Add the symbol:data pair to the plant_dict
    data = table_df[0].iloc[:,1]
    plant_dict[symbol] = data.to_list()

    

#Get a list all unique index values 
list_of_indexes = [index_series.to_list() for index_series in list_of_indexes]
flat_list_of_indexs = [item for sublist in list_of_indexes for item in sublist]
full_index = list(set(flat_list_of_indexs))


#A list of each plant's data, indexed by the index grabbed from the plants df in the for loop
list_of_values_series = [pd.Series(value_list,index=index) for value_list,index in zip(list(plant_dict.values()),list_of_indexes)]

#Fill na's for a index values not in the full index
for series in list_of_values_series:
    missing_characteristics = set(full_index).difference(set(series.index))
    if missing_characteristics != {}:
        for missing_characteristic in missing_characteristics:
            series[missing_characteristic] = np.NaN
    series.reindex(full_index)

df = pd.DataFrame(index=full_index)

#Create a column in the df for each plant
remaining_symbols = list(plant_dict.keys())
for index,symbol in enumerate(remaining_symbols):
    print(index)
    df[symbol] = list_of_values_series[index]

#Transpose so each row is a plant, and make symbol a column

df = df.T.reset_index()
df.rename({"index":"USDA_Symbol"},axis=1,inplace=True)

#Left Join with symbols 
symbols = pd.read_csv("symbols.csv")
symbols.columns = ["USDA_Symbol"]

final_df = pd.merge(symbols,df,on="USDA_Symbol",how="left")  





final_df.to_csv("USDAPlantCharacteristics.csv")


    






















