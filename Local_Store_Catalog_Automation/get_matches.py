import pandas as pd
import os

era_pa = pd.read_excel("PA Wildflower Database.xlsx",sheet_name="ERA_PA")
era_pa = era_pa[["Scientific Name","Common Name","USDA Symbol"]]

for col in era_pa:
    era_pa[col] = era_pa[col].str.lower()


count_dict = {}
list_of_dfs = []

for file in os.listdir("./TextFiles"):

    full_path = "./TextFiles/" + file

    with open(full_path,encoding='unicode_escape') as f:
        string = f.read()
    
    df = era_pa.copy()
    df["Match"] = 0

    com_names = df["Common Name"].to_list()
    scientific_names = df["Scientific Name"].to_list()

    for i,tup in enumerate(list(zip(com_names,scientific_names))):
        common_name = tup[0]
        scientific_name = tup[1]
        if ((common_name in string) | (scientific_name in string)):
            df.loc[i,"Match"] = 1

    nursery = file.split(".")[0]
    df["Nursery"] = nursery
    
    
    df = df[df.Match == 1]

    count = df.Match.sum()
    count_dict.update({nursery:count})

    df.drop("Match",axis=1,inplace=True)
    list_of_dfs.append(df)


nursery_matches = pd.concat(list_of_dfs)
nursery_matches.to_csv("Local_Long.csv")

count_df = pd.DataFrame(index = count_dict.keys(), data=count_dict.values(),columns=["Counts"])
count_df.to_csv("Counts.csv")
    
    



