import requests
from bs4 import BeautifulSoup
import pandas as pd


HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
}

path = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\Local_Store_Catalog_Automation\PA Wildflower Database.xlsx"
data = pd.read_excel(path,sheet_name="ERA_PA")
symbols = data["USDA Symbol"].to_list()
scientific_names = data["Scientific Name"].str.lower().to_list()

response = requests.get("https://www.fs.fed.us/wildflowers/plant-of-the-week/index.php?profiles=all",headers=HEADERS)

soup = BeautifulSoup(response.text,features='lxml')


temp = soup.select("a[href^='/wildflowers/plant-of-the-week']")

plants = [element.find_next_sibling() for element in temp]
plants = pd.Series([item.text.lower() for item in plants if item is not None])

#111
print(plants.isin(scientific_names).sum())

