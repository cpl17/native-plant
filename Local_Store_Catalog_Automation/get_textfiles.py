from numpy import append
import pandas as pd
from utils import get_text_file_pdf,get_text_file_html,get_text_file_rtf,get_text_file_docx,get_text_file_doc,get_text_file_excel
from scrapers import get_hungry_urls
import os
import shutil

# Dataframe of nurseries and the relevant urls where each availability listing is hosted
catalog_df = pd.read_excel("./Data/PA Wildflower Database.xlsx",sheet_name="Local_Catalog_URLS")
catalog_df = catalog_df.loc[(catalog_df["Solved"] == "Yes"),["Nursery","Catalog URLS"]]


# GroupBy Nursery to create a list of urls for each nursery (if they're are muliple)
# Store nurseries and urls in a dict

catalog_df_grouped = catalog_df.groupby("Nursery")["Catalog URLS"].apply(lambda x:",".join(x).split(","))
catalog_dict = catalog_df_grouped.to_dict()



# Create a temporary folder for data to be written to
if not os.path.exists(os.path.abspath('tmp')):
    os.mkdir("tmp")

# Create a folder for final text files to be written to
if not os.path.exists(os.path.abspath('Data/TextFiles')):
    os.mkdir("Data/TextFiles")


# Iterate though the catalog dictionary. If there is a normal file extension (pdf, html etc) then the url
# is caught in the if/then logic, and the corresponding method is used. However, I'm using a hacky solution for a few edge case urls
# that don't fall neatly into this logic ()
for nursery,urls in catalog_dict.items():



    if nursery == "Hungry Hook Bainbridge":
        urls = get_hungry_urls(urls[0])

    # Iterate through each url, impliment the method and write/append to the text file
    append = False
    for i,url in enumerate(urls):

        #The "extension" is a file extension if there is one. Else its text to the right of the last period
        extension = url.split(".")[-1]

        print(extension)

        #If there are multiple urls, append the text to the end of the file. Clearly delimit each text from
        #source
        if i > 0:
            append = True
            with open(f"Data/TextFiles/{nursery}.txt","a",encoding='utf-8') as f:
                f.write("\n\nNew File\n\n")
    
         
        ##Irregular extensions##
        if ("download/price-list" in extension):
            get_text_file_pdf(url,nursery,append)

        elif (("onedrive" in url) & (nursery == "Archewild Quakertown")):  #Archewild download link
            #LINK BROKEN
            # get_text_file_excel(url,nursery,append)
            continue
        
        ##Regular Extensions##
        elif (extension == "pdf"):
            get_text_file_pdf(url,nursery,append)

        elif extension == "html":
            get_text_file_html(url,nursery,append)
        elif extension == "rtf":
            get_text_file_rtf(url,nursery,append)
          
        elif extension == "docx":
            get_text_file_docx(url,nursery,append)
            
        elif extension == "doc":
            get_text_file_doc(url,nursery,append)
        
        elif extension == "xlsx":
            get_text_file_excel(url,nursery,append)
        
        ##Web Pages##
        elif extension.find("/") != -1:
            get_text_file_html(url,nursery,append)
        else:
            print(f"{nursery} not being caught")
            


try:
    shutil.rmtree('tmp')
except OSError as e:
    print("Error: %s : %s" % ("tmp", e.strerror))