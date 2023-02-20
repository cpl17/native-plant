from numpy import append
import pandas as pd
from utils import get_text_file_pdf,get_text_file_html,get_text_file_excel
import os
import shutil

# Dataframe of nurseries and the relevant urls where each availability listing is hosted
catalog_df = pd.read_excel("./Data/Local_Catalog_URLs_2_20.xlsx",sheet_name="Sheet1")
catalog_df = catalog_df.loc[(catalog_df["Type"].isin(["PDF","HTML","EXCEL"])),["Nursery","Catalog_URLS","Type"]]

print(catalog_df)


# GroupBy Nursery to create a list of urls for each nursery (if they're are muliple)
# Store nurseries and urls in a dict

catalog_df_grouped = pd.DataFrame(catalog_df.groupby(["Nursery","Type"])["Catalog_URLS"].apply(lambda x:",".join(x).split(",")))
catalog_df_grouped.reset_index(level=1,inplace=True)

print(catalog_df_grouped)



# Create a temporary folder for data to be written to
if not os.path.exists(os.path.abspath('tmp')):
    os.mkdir("tmp")

# Create a folder for final text files to be written to
if not os.path.exists(os.path.abspath('Data/TextFiles')):
    os.mkdir("Data/TextFiles")


# Iterate though the catalog dictionary. If there is a normal file extension (pdf, html etc) then the url
# is caught in the if/then logic, and the corresponding method is used. However, I'm using a hacky solution for a few edge case urls
# that don't fall neatly into this logic ()


for nursery in catalog_df_grouped.index:
    
    print(nursery)

    Type, urls = catalog_df_grouped.loc[nursery].to_list()

    for i, url in enumerate(urls):

        if Type == "HTML":
            try:
                get_text_file_html(url,nursery,append) 
            except Exception as e:
                print(f"Nursery failed with error: {e}")

        elif Type == "PDF":
            try:
                get_text_file_pdf(url,nursery,append) 
            except Exception as e:
                print(f"Nursery failed with error: {e}")


        elif Type == "EXCEL":
            try:
                get_text_file_excel(url,nursery,append) 
            except Exception as e:
                print(f"Nursery failed with error: {e}")    
        else:
            print(Type)
            print(f"{nursery} not being caught")  

        #If there are multiple urls, append the text to the end of the file. Clearly delimit each text from
        #source
        if i > 0:
            append = True
            with open(f"Data/TextFiles/{nursery}.txt","a",encoding='utf-8') as f:
                f.write("\n\nNew File\n\n")


try:
    shutil.rmtree('tmp')
except OSError as e:
    print("Error: %s : %s" % ("tmp", e.strerror))