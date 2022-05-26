import pandas as pd
from utils import get_text_file_pdf,get_text_file_html,get_text_file_rtf,get_text_file_docx,get_text_file_doc
from scrapers import get_gino_urls
import os
import shutil

HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Chrome/87.0.4280.141"
}

# Catalog Reference
catalog_df = pd.read_excel("PA Wildflower Database.xlsx",sheet_name="Local_Catalog_URLS")
catalog_df = catalog_df.loc[(catalog_df["Solved"] == "Yes"),["Nursery","Catalog URLS"]]

# GroupBy Nursery to create list of urls (if they're are muliple)

catalog_df_grouped = catalog_df.groupby("Nursery")["Catalog URLS"].apply(lambda x:",".join(x).split(","))
catalog_dict = catalog_df_grouped.to_dict()



if not os.path.exists(os.path.abspath('tmp')):
    os.mkdir("tmp")

for nursery,urls in catalog_dict.items():
    
    if nursery == "Gino's Newtown":
        urls = get_gino_urls(urls[0])
    

    append = False
    for i,url in enumerate(urls):
        extension = url.split(".")[-1]

        if i > 0:
            append = True

        if ((extension == "pdf") | ("download/price-list" in extension)):
            
            get_text_file_pdf(url,nursery,append)
        elif extension == "html":
            get_text_file_html(url,nursery,append)
        elif extension == "rtf":
            get_text_file_rtf(url,nursery,append)
          
        elif extension == "docx":
            get_text_file_docx(url,nursery,append)
            
        elif extension == "doc":
            get_text_file_doc(url,nursery,append)
        elif extension.find("/") != -1:
            get_text_file_html(url,nursery,append)
        else:
            print(extension)
            


try:
    shutil.rmtree('tmp')
except OSError as e:
    print("Error: %s : %s" % ("tmp", e.strerror))







