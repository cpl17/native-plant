import pandas as pd
import os

#The source database
era_pa = pd.read_excel("./Data/PA Wildflower Database.xlsx",sheet_name="ERA_PA")
era_pa = era_pa[["Scientific Name","Common Name","USDA Symbol"]]

for col in era_pa:
    era_pa[col] = era_pa[col].str.lower()


count_dict = {}
list_of_dfs = []

#For each file -> read file into string,check common and scientific names for each plant against the string. Using acopy of the 
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

#A long df with entries SYMBOL NURSERY URL. Note: URLS are the nursery urls NOT the 
# urls used for the http requests. 
nursery_matches = pd.concat(list_of_dfs)

nursery_info = pd.read_excel("./Data/PA Wildflower Database.xlsx",sheet_name="Local_Catalog_URLS")
nursery_info = nursery_info.loc[(nursery_info["Solved"] == "Yes"),["Nursery","Nursery URL"]].drop_duplicates(subset="Nursery")
mapping = nursery_info.set_index("Nursery").to_dict()["Nursery URL"]

nursery_matches["URL"] = nursery_matches["Nursery"].map(mapping)
nursery_matches = nursery_matches[["USDA Symbol","Nursery","URL"]]
nursery_matches.to_csv("./Data/Local_Long.csv")

#Aggegrate along symbol to get SYMBOL URLS COUNT df. 
nursery_matches["URL"] = nursery_matches["Nursery"].map(mapping)
df = nursery_matches[["USDA Symbol","Nursery","URL"]]

f = lambda x: ', '.join(map(str, set(x)))
local_agg = df.groupby("USDA Symbol").agg({"URL":[f,len]})
local_agg.reset_index(inplace=True)
local_agg.columns = ["USDA Symbol","URLS","COUNT"]
local_agg.to_csv("./Data/Local_Agg.csv")


#Count dict -> DataFrame
count_df = pd.DataFrame(index = count_dict.keys(), data=count_dict.values(),columns=["Counts"])
count_df.to_csv("./Data/Counts.csv")
    
    



