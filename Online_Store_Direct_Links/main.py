import pandas as pd 

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException,TimeoutException,WebDriverException
from bs4 import BeautifulSoup
import os

PATH = "C:\Program Files (x86)\chromedriver.exe"
DELAY = 2



#Metadata and Source Data
era_pa = pd.read_excel("./Data/PA Wildflower Database.xlsx",sheet_name="ERA_PA")
data = pd.read_excel("./Data/PA Wildflower Database.xlsx",sheet_name="ONLINE")

map = era_pa[["USDA Symbol","Common Name"]]
map = map.set_index("USDA Symbol").to_dict()["Common Name"]
data["Common Name"] = data["USDA"].map(map)

data = data.sample(frac=1)

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

for row in data.iterrows():

    link_directs_correctly = False

    #These are not returning enough solutions to take the time to include them
    if row[1].Root in ["PlantMoreNatives.com","MidAtlanticNatives.com"]:
        links_final.append(row[1].Root)
        count += 1
        print(count)
        continue

    #Iterate through each of the options (Direct -> DuckDuckGo -> Search Tool)
    for link_type,link in zip(["Direct","Duck","Search"],[row[1].Direct,row[1].Duck,row[1].Search]):


        #Ignore if link missing
        #When read in through pandas "NA" -> missing (is a float type)
        if (link == "NA") | isinstance(link,float):
            continue

        #Meadlowlands blocks ip after a certain number of requests
        try:
            driver.get(link)
        except WebDriverException:
            continue

        #Wait for page to load
        try:  
            WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.TAG_NAME,"div")))
        except TimeoutException:
            print(f"{link} did not have a div or there was an error")
            continue

        #Set Variables for checks

        url = driver.current_url.lower()
        page_source = driver.page_source.lower()
    

        #DuckDuckGo gets mad when you do too many of these queries. In this case, the links resolves to an error page or duckduck search results. Both satisify the criteries 
        # and will be marked as a match. Since the url doesn't change, we can notice this using the following logic. 
        if url in [link,link.lower()]:
            continue

        #Assumes if the scientific or common names are on the page sources -> correct site
        if (row[1]["Scientific Name"].lower() in page_source) | (row[1]["Common Name"].lower() in page_source) :
            link_directs_correctly = True

        ###Conditions where the text is on the page but it's not the correct site###

        if not row[1].Root.lower() in url:
            link_directs_correctly = False

        #ErnstSeed eccentricities
        if "pdf" in url:
            link_directs_correctly = False

        if "0 products" in page_source:
            link_directs_correctly = False

        #IzelPlants eccentricities   
        if "Your search return no results" in page_source:
            link_directs_correctly = False

     
       #Prairiemoon eccentricities
        if (link_type != "Direct") & (row[1].Root == "PrairieMoon.com"):
            
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,"results-title.ng-scope")))
            except TimeoutException:
                link_directs_correctly = False
                continue

        #If link direct correctly, append to list of links and move to next plant, else move to next link. 
        if link_directs_correctly: 
            links_final.append(link)
            break

    if not link_directs_correctly:

        links_final.append(row[1].Root)
    
    count += 1
    print(count)

    #Exit Program if duckduckgo error occurs
    if sum([1 if "duck" in url else 0 for url in links_final[-10:]]) == 10:
        with open("links_final.txt","w") as f:
            for link in links_final:
                f.write(link)
        driver.close()
        os.exit()


data["Final"] = links_final
data.to_csv("./Data/Online_NEW_Final.csv")


data["Match"] = (data["Final"] != data["Root"] )
data.sort_values(by="Root",inplace=True)
data.to_csv("./Data/Online_NEW_2.csv")