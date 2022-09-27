import requests 
import pandas as pd

era_pa = pd.read_excel("./Data/PA Wildflower Database.xlsx",sheet_name="ERA_PA")
data = era_pa[["USDA Symbol","Scientific Name","Common Name"]]

matches = []
urls = []

for name in data["Scientific Name"].to_list():
    test_url = f"https://www.toadshade.com/{'-'.join(name.split())}.html"
    response = requests.get(test_url)
    status_code = response.status_code
    if status_code == 200:
        matches.append(name)
        urls.append(response.url)


pd.DataFrame({"Scientific Name":matches,"URL":urls}).to_csv("ToadShade_Final.csv")
