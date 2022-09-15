import requests
import pandas as pd

HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
}

path = r"C:\Users\CPL17\OneDrive\Documents\Code\Dev Projects\Current\Local_Store_Catalog_Automation\PA Wildflower Database.xlsx"
data = pd.read_excel(path,sheet_name="ERA_PA")[["USDA Symbol","Scientific Name","Common Name"]]
symbols = data["USDA Symbol"].to_list()
scientific_names = data["Scientific Name"].to_list()
common_names = data["Common Name"].to_list()

df_list = []


############# Wilflower ########################

base_url = "https://www.wildflower.org/plants/result.php?id_plant="
urls = [base_url + symbol for symbol in symbols]

list_of_records = []

for symbol,url in list(zip(symbols,urls)):
    if requests.get(url,headers=HEADERS).status_code == 200:
        list_of_records.append([symbol,url])

df_list.append(pd.DataFrame(list_of_records))

###################### USDA PLANTS #####################

base_url = "https://plants.usda.gov/home/plantProfile?symbol="
urls = [base_url + symbol for symbol in symbols]

list_of_records = []

for symbol,url in list(zip(symbols,urls)):
    if requests.get(url,headers=HEADERS).status_code == 200:
        list_of_records.append([symbol,url])

df_list.append(pd.DataFrame(list_of_records))


###################### USDA Forest Service #####################


names_for_us_forest = ["_".join(x.lower().split()) for x in scientific_names]
urls = [f"https://www.fs.fed.us/wildflowers/plant-of-the-week/{name}.shtml" for name in names_for_us_forest]


list_of_records = []

for symbol,url in list(zip(symbols,urls)):
    if requests.get(url,headers=HEADERS).status_code == 200:
        list_of_records.append([symbol,url])

df_list.append(pd.DataFrame(list_of_records))


######################## BONAP ####################### 

names_for_bonap = ["%20".join(sci_name.split()) for sci_name in scientific_names]
urls = [f"http://bonap.net/MapGallery/County/{name}.png" for name in names_for_bonap]

list_of_records = []

for symbol,url in list(zip(symbols,urls)):
    if requests.get(url,headers=HEADERS).status_code == 200:
        list_of_records.append([symbol,url])

df_list.append(pd.DataFrame(list_of_records))


#Mt. Cuba - MAYBE

common_names = list(map(lambda x: "-".join(x.lower().split()),common_names))

base_url = "https://mtcubacenter.org/plants/"
urls = [base_url + common_name for common_name in common_names]

list_of_records = []

for symbol,url in list(zip(symbols,urls)):

    response = requests.get(url,headers=HEADERS)
    if symbol in response.text:
        list_of_records.append([symbol,url])        

df_list.append(pd.DataFrame(list_of_records))


full_df = pd.concat(df_list)
full_df.columns = ["USDA Symbol","URL"]
full_df.to_csv("long.csv")


#Aggregate 

f = lambda x: ', '.join(x)
agg = full_df.groupby("USDA Symbol").agg({"URL":list})
agg.reset_index(inplace=True)
agg.columns = ["USDA Symbol","URLs"]
agg.to_csv("agg.csv")







#TODO: Make a reference list of symbol, common, name, and 