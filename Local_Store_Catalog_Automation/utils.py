import requests
from bs4 import BeautifulSoup
import re
import pdfplumber
import pandas as pd
import docx
from striprtf.striprtf import rtf_to_text
import win32com.client 
import os
import re


HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Chrome/87.0.4280.141"
}

def get_text_file_html(url,nursery_name,append):

    response = requests.get(url = url, headers = HEADERS)
    page = response.text

    soup = BeautifulSoup(page,features='html.parser') 
    text = re.sub('\n',' ',soup.text)
    

    text = text.lower()

    if ((nursery_name == "Earthbound Ephrata") | (nursery_name == "Hungry Hook Bainbridge")):
        text = page.lower()

    if append:
            
        with open(f"TextFiles/{nursery_name}.txt","a",encoding='utf-8') as f:
            f.write(text)
    else:
        with open(f"TextFiles/{nursery_name}.txt","w",encoding='utf-8') as f:
            f.write(text)
  


def get_text_file_pdf(url,nursery_name,append):

    response = requests.get(url = url, headers = HEADERS)

    #Write Binary 
    with open('tmp/catalog.pdf', 'wb') as f:
        f.write(response.content)


    #Write Concatenated string to text file
    with pdfplumber.open('tmp/catalog.pdf') as pdf:
        pages = pdf.pages
        text = ""
        for page in pages:
            text += page.extract_text()

    text = text.lower()

    if append:
            
        with open(f"TextFiles/{nursery_name}.txt","a",encoding='utf-8') as f:
            f.write(text)
    else:
        with open(f"TextFiles/{nursery_name}.txt","w",encoding='utf-8') as f:
            f.write(text)


def get_text_file_docx(url,nursery_name,append):

    
    response = requests.get(url = url, headers = HEADERS)

    #Write Binary to .docx
    with open('tmp/catalog.docx', 'wb') as f:
        f.write(response.content)

    #Read Docx 

    doc = docx.Document('tmp/catalog.docx')
    text = ""
    for docpara in doc.paragraphs:
        text += docpara.text
    text = text.lower()

    if append:
            
        with open(f"TextFiles/{nursery_name}.txt","a") as f:
            f.write(text)
    else:
        with open(f"TextFiles/{nursery_name}.txt","w") as f:
            f.write(text)   



def get_text_file_rtf(url,nursery_name,append):

    
    response = requests.get(url = url, headers = HEADERS)

    #Write Binary to .rtf
    with open('tmp/catalog.rtf', 'wb') as f:
        f.write(response.content)

    #Strip embeddings from rtf; store as text string

    with open('tmp/catalog.rtf') as f:
        text = rtf_to_text(f.read())
    
    text = text.lower()

    
    #Write string to text file 
    if append:

        with open(f"TextFiles/{nursery_name}.txt","a") as f:
            f.write(text)
    else:
        with open(f"TextFiles/{nursery_name}.txt","w") as f:
            f.write(text)   


def get_text_file_doc(url,nursery_name,append):

    response = requests.get(url = url, headers = HEADERS)

    #Write Binary to .docx
    with open('tmp/catalog.doc', 'wb') as f:
        f.write(response.content)


    #Use COM client to convert to .docx

    word = win32com.client.Dispatch("Word.Application")
    in_file = os.path.abspath('tmp/catalog.doc')
    wb = word.Documents.Open(in_file)
    out_file = os.path.abspath("tmp/catalog.docx")
    wb.SaveAs2(out_file, FileFormat=16) # file format for docx
    wb.Close()


    #Read Docx 
    doc = docx.Document('tmp/catalog.docx')
    text = ""
    for docpara in doc.paragraphs:
        text += docpara.text
    text = text.lower()
        
    #Write to TextFiles
    if append:
             
        with open(f"TextFiles/{nursery_name}.txt","a") as f:
            f.write(text)
    else:
        with open(f"TextFiles/{nursery_name}.txt","w") as f:
            f.write(text)  





    