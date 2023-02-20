import pandas as pd
import os

PATH_TO_DB = r"C:\Users\CPL17\OneDrive\Desktop\PA Wildflower Database 10_27.xlsx"
PATH_TO_CATALOG_URLS = "./Data/Local_Catalog_URLs_2_20.xlsx"

#The source database
era_pa = pd.read_excel(PATH_TO_DB,sheet_name="ERA_PA")
era_pa = era_pa[["Scientific Name","Common Name","USDA Symbol"]]

for col in era_pa:
    era_pa[col] = era_pa[col].str.lower()


count_dict = {}
list_of_dfs = []

#For each file -> read file into string,check common and scientific names for each plant against the string. Using a copy of the 
# source dataframe, remove all non-matched values,  and append to a list

for file in os.listdir("./Data/TextFiles"):

    full_path = "./Data/TextFiles/" + file

    with open(full_path,encoding='unicode_escape') as f:
        string = f.read()
    
    df = era_pa.copy()
    df["Match"] = 0

    com_names = df["Common Name"].to_list()
    scientific_names = df["Scientific Name"].to_list()


    #Check the string for the common name and scientific name. 
    # If there is a match, replace match with a 1
    for i,tup in enumerate(list(zip(com_names,scientific_names))):
        common_name = tup[0]
        scientific_name = tup[1]
        if ((common_name in string) | (scientific_name in string)):
            df.loc[i,"Match"] = 1

    #Create a nursery column
    nursery = file.split(".")[0]
    df["Nursery"] = nursery
    
    #Reduce the df to only where there is a match
    df = df[df.Match == 1]

    #Find the number of matches and append to the count dict
    count = df.Match.sum()
    count_dict.update({nursery:count})

    df.drop("Match",axis=1,inplace=True)
    list_of_dfs.append(df)

####A long df with entries SYMBOL Catalog URLS. Note: URLS are the Catalog URLSs NOT the 
# urls used for the http requests. 

nursery_matches = pd.concat(list_of_dfs)

#Clean up
nursery_matches.columns = ["Scientific Name","Common Name","USDA_Symbol","SOURCE"]
nursery_matches["USDA_Symbol"] = nursery_matches["USDA_Symbol"].str.upper()
nursery_matches["Common Name"] = nursery_matches["Common Name"].str.title()
nursery_matches["Scientific Name"] = nursery_matches["Scientific Name"].str.title()

#Regain the urls 
nursery_info = pd.read_excel(PATH_TO_CATALOG_URLS,sheet_name="Sheet1") 
nursery_info = nursery_info[["Nursery","Root_URL"]].drop_duplicates(subset="Nursery")
mapping = nursery_info.set_index("Nursery").to_dict()["Root_URL"]
nursery_matches["SOURCE_URL"] = nursery_matches["SOURCE"].map(mapping) 

df = nursery_matches.drop(["Scientific Name","Common Name"],axis=1)
df.columns = ["USDA_SYMBOL","SOURCE","SOURCE_URL"]
df.to_csv("./Data/Local_Long.csv",index=False)

####Aggregate along symbol to get SYMBOL URLS COUNT df. 

#Aggregate by creating a comma separated string for both SOURCE and SOURCE_URL
f = lambda x: ', '.join(map(str, set(x)))
local_agg = nursery_matches.groupby("USDA_Symbol").agg({"SOURCE_URL":[f,len],"SOURCE":f})

local_agg.reset_index(inplace=True)
local_agg = local_agg["USDA_Symbol","SOURCE_URLS","COUNT","SOURCE"]
local_agg = pd.merge(local_agg,nursery_matches[["USDA_Symbol","Scientific Name","Common Name"]].drop_duplicates(),how="left",on="USDA_Symbol")

local_agg["String"] = local_agg["Scientific Name"] + " (" + local_agg["Common Name"] + "): " + local_agg["SOURCE"]
local_agg.columns = ["USDA_Symbol","SOURCE","SOURCE_URLS","COUNT","Scientific Name","Common Name","String"]
local_agg.to_csv("./Data/Local_Agg.csv",index=False)

#Count dict -> DataFrame
count_df = pd.DataFrame(index = count_dict.keys(), data=count_dict.values(),columns=["Counts"])
count_df.to_csv("./Data/Counts.csv")
    
    




