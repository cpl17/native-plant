from bs4 import BeautifulSoup
import requests 
import re
import pandas as pd
import numpy as np
from collections import defaultdict
import time


# Global Constansts

BASE_URL = "https://www.wildflower.org/plants/result.php?id_plant="
HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Chrome/87.0.4280.141"
}

# Functions 


# Each section (Bloom Information, Growing Conditions) on the page is a div. The characteristic(s) i.e. "Bloom Color", are all emphasized and hence caught between 
# strong tags. Similarly, their values i.e. "Red" follow the end of strong tags and preceed a line break. 
# This function finds all characteristics/labels and their relevant values and stores the pairs in a dictionary as follows:
# {'characteristic':'value','characteristic':'value}. 
# Returns empty dict if div does not contain the relevant information

def get_info(string):

    #Remove Tags from column labels ie "Bloom Color"

    def clean_column_labels(string):
        return string.replace("<strong>","").replace("</strong>","").replace(":","")

    #Remove Tags from column values ie "Red"
    
    def clean_column_values(string):
        new_string = string.replace("</strong>","").replace("<br/>","")
        new_string = ",".join(new_string.split(" , "))
        return new_string
    
    #Remove the hyperlink text 
    string = re.sub("<a.*?>","",str(string))
    string = re.sub("</a>","",string)

    #Catch Column Lables
    lst1 = re.findall("<strong>[\w\s]+:<\/strong>",string)
    lst1_cleaned = [clean_column_labels(x) for x in lst1]

    #Catch Column Values
    lst2 = re.findall("<\/strong>[\w\s\\.\-\,]+<br\/>",string)
    lst2_cleaned = [clean_column_values(x) for x in lst2]

    section_dict = dict(zip(lst1_cleaned,lst2_cleaned))

    return section_dict


# Functions for cleaning specific columns of the scraped data # 

def clean_color(x):
    if not isinstance(x,float):
        x = x.strip()
        x = x.split(",")
        if len(x) == 2:
            return "–".join(x)
        else:
            return ", ".join(x)
    else:
        return x

def clean_bloom(x):
    if not isinstance(x,float):
        x = x.strip()
        x = x.split(",")
        return x[0] + "–" + x[-1]       
    else:
        return x

def clean_size(x):
    if not isinstance(x,float):
        size = x.strip()
        size = size.replace(" ft.","").strip()

        # There are times were two size ranges are given (happens 5 times so ignore)
        if len(size.split(",")) > 1:
            return np.NaN
        else:
            size = "–".join(size.split("-"))
            return size 
    else:
        return x

add_space = lambda x : (", ".join(x.split(","))).strip() if not isinstance(x,float) else x


############################################################################################

# Load data and reduce to relevant columns and rows with missing values 
data_full = pd.read_csv("ERA_PA.csv")


identifiers = ["Quick Lookup","USDA Symbol","Scientific Name","Common Name"]
fields_wth_missing = [ "Flower Color", "Flowering Months", "Height (feet)", "Sun Exposure", "Soil Moisture" ]
data_relevant = data_full[identifiers + fields_wth_missing]


# List of USDA symbols (the pk in the databasee) to query over 
idx = data_relevant[fields_wth_missing].isna().any(axis=1)
symbols = data_relevant.loc[idx,"USDA Symbol"].to_list()


# Empty dict that will be populated with a dict for each symbol
plant_dict = defaultdict(dict)

counter = 0
for symbol in symbols:

    # Get the Page text for the symbol using http request module
    full_url = BASE_URL + symbol
    response = requests.get(url = full_url, headers = HEADERS)
    page = response.text 
    
    # Find the relevant sections of the page
    soup = BeautifulSoup(page,features='lxml')
    stuff = soup.find_all("div",class_="section")

    # When the symbol is not found on the website it returns a page with 2 divs matching the searched for criteria

    if len(stuff) > 2:

        for string in stuff:
            
            if plant_dict[symbol] is None:
                plant_dict[symbol] = get_info(string)
            else:
                # This combines all the k/v pairs on the page into a single dict and deals with empty dicts
                plant_dict[symbol].update(get_info(string))
    
    counter += 1
    if counter % 100 == 0:
        print(counter)

    time.sleep(1)



# Cast as df and transpose because symbols originally index columns        
temp = pd.DataFrame(plant_dict).T
data = temp[["Bloom Color","Bloom Time","Size Class","Light Requirement","Soil Moisture"]]
data.columns = ["Flower Color", "Flowering Months", "Height (feet)", "Sun Exposure", "Soil Moisture" ]




#Use helpers to clean data
list_of_funcs = [clean_color,clean_bloom,clean_size,add_space,add_space]
for col,fun in list(zip(data.columns,list_of_funcs)):
    data[col] = data[col].apply(fun)

data.to_csv("scraped_data.csv")

# data = pd.read_csv("scraped_data.csv")

# Join scraped data with original data; creates duplicated columns _x for orginal, _y for data from scraped 

data = data.reset_index().rename({"index":"USDA Symbol"},axis=1)
temp = data_relevant.merge(data,on="USDA Symbol",how='left')

#Replace Missing Values - use scraped value if missing in original data set

for col in fields_wth_missing:
    col_org = col + "_x"; col_scraped = col + "_y"

    idx = temp[col_org].isna()
    temp.loc[idx,col_org] = temp.loc[idx,col_scraped]

# Select columns and  Write to excel 
final = temp.drop(["Flowering Months_y","Flower Color_y","Height (feet)_y","Sun Exposure_y","Soil Moisture_y"],axis=1)
final.columns = identifiers + fields_wth_missing


# Replace columns in original df 

final.to_excel("FINAL.xlsx")





