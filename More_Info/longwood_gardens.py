import requests 
import pandas as pd

HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
}

path = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\Local_Store_Catalog_Automation\PA Wildflower Database.xlsx"
data = pd.read_excel(path,sheet_name="ERA_PA")
symbols = data["USDA Symbol"].to_list()
scientific_names = data["Scientific Name"].to_list()

num = 0
no_server_error = True
while no_server_error:

    url = f"https://plantexplorer.longwoodgardens.org/weboi/oecgi2.exe/INET_ECM_DispPl?NAMENUM={num}&DETAIL=1&startpage=1"

    #Get Stuff 
