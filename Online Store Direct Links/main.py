import pandas as pd 

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from bs4 import BeautifulSoup

PATH = "C:\Program Files (x86)\chromedriver.exe"
DELAY = 2



#Metadata and Source Data
era_pa = pd.read_excel("PA Wildflower Database.xlsx",sheet_name="ERA_PA")
data = pd.read_excel("PA Wildflower Database.xlsx",sheet_name="ONLINE")

map = era_pa[["USDA Symbol","Common Name"]]
map = map.set_index("USDA Symbol").to_dict()["Common Name"]
data["Common Name"] = data["USDA"].map(map)



#Get Direct Links - These links follow the most commonly used structure that each nursery uses for the pages for each plant. Link failures are from using different common names (a common occurence) and a different structure.

direct_links = []
root = data["Root"].to_list()


for row in data.iterrows():

    if row[1]["Root"] == "ErnstSeed.com":
        direct_link = "https://www.ernstseed.com/product/" + "-".join(row[1]["Common Name"].lower().split())
    
    elif row[1]["Root"] == "IzelPlants.com":
        direct_link = "https://www.izelplants.com/" + "-".join(row[1]["Scientific Name"].lower().split()) + "-" + "-".join(row[1]["Common Name"].lower().split())

    elif row[1]["Root"] == "ToadShade.com":
        direct_link = "https://toadshade.com/" +  ("-".join(row[1]["Scientific Name"].lower().split())).capitalize() + ".html"


    elif row[1]["Root"] == "MidAtlanticNatives.com":
        direct_link = "https://midatlanticnatives.com/product/" + "-".join(row[1]["Scientific Name"].lower().split()) + "-" + "-".join(row[1]["Common Name"].lower().split())

    elif row[1]["Root"] == "PrairieMoon.com":
        direct_link = "https://www.prairiemoon.com/"+ "-".join(row[1]["Scientific Name"].lower().split()) + "-" + "-".join(row[1]["Common Name"].lower().split())+ "-prairie-moon-nursery.html"

    else:
        direct_link = "NA"

    direct_links.append(direct_link)


#Get Search Links - These links use the url for the sites search tool (if they have one).

search_links = []
root = data["Root"].to_list()


for row in data.iterrows():

    if row[1]["Root"] == "ErnstSeed.com":
        scientific_name = ("%20".join(row[1]["Scientific Name"].split())).lower()
        common_name = ("%20".join(row[1]["Common Name"].split())).lower()
        search_link = f"https://www.ernstseed.com/seed-finder-tool/?s=&CommonName={common_name}&ItemNumber=&Botanical_Name={scientific_name}"
    
    elif row[1]["Root"] == "IzelPlants.com":
        scientific_name = ("%20".join(row[1]["Scientific Name"].split())).lower()
        search_link = f"https://www.izelplants.com/catalogsearch/result/?q={scientific_name}"

    elif row[1]["Root"] == "ToadShade.com":
        search_link = "NA"

    elif row[1]["Root"] == "MidAtlanticNatives.com":
        search_link = "NA"



    elif row[1]["Root"] == "PrairieMoon.com":
        
        scientific_name = ("%20".join(row[1]["Scientific Name"].split())).lower()
        search_link = f"https://www.prairiemoon.com/search.html?Search={scientific_name}"

    else:
        search_link = "NA"

    search_links.append(search_link)

# Add link columns and rename/reorder
data["Direct"] = direct_links
data["Search"] = search_links
data = data[["USDA","Scientific Name","Common Name","Root","Web","Direct","Search"]]
data.columns = ["USDA","Scientific Name","Common Name","Root","Duck","Direct","Search"]

# Find the final links


driver = webdriver.Chrome(executable_path=PATH)

links_final = []

count = 0
print(data.shape)

for row in data.sample(100).iterrows():
 
    #Iterate through each of the options (Direct -> DuckDuckGo -> Search Tool)
    for link in [row[1].Direct,row[1].Duck,row[1].Search]:

        if link == "NA":
            continue

        #Write current links to a csv in case of a time out exception
        try:

            driver.get(link)
        
        except TimeoutException:

            pd.Series(links_final).to_csv("Links")


        link_directs_correctly = False

        #Assumes if text on page correct site
        if (row[1]["Scientific Name"].lower() in driver.page_source.lower()) | (row[1]["Common Name"].lower() in driver.page_source.lower()) :
            link_directs_correctly = True

        ###Conditions where the text is on the page but it's not the correct site###

        if not row[1].Root.lower() in driver.current_url.lower():
            link_directs_correctly = False

        #ErnstSeed eccentricities
        if "pdf" in driver.current_url.lower():
            link_directs_correctly = False

        if "0 products" in driver.page_source.lower():
            link_directs_correctly = False

        #IzelPlants eccentricities   
        if "Your search return no results" in driver.page_source.lower():
            link_directs_correctly = False

        #Prairiemoon eccentricities
        if "returned no results" in driver.page_source.lower():
            link_directs_correctly = False

        #If link direct correctly, move to next plant, else move to next link. 
        if link_directs_correctly:

            links_final.append(link)
            break

    if not link_directs_correctly:

        links_final.append(row[1].Root)
    
    count += 1

    print(count)


    

data["Final"] = links_final
data["Match"] = data["Final"] != data["Root"] 
data.sort_values(by="Root",inplace=True)
data.to_csv("Online_NEW.csv")