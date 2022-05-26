from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException

PATH = "C:\Program Files (x86)\chromedriver.exe"
DELAY = 3


# def get_hungry_urls(url):

#     driver = webdriver.Chrome(executable_path=PATH)

#     # Open Page 
#     driver.get(url)

#     # Get Link texts 

#     try:
#         WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.LINK_TEXT, "All Items")))
#     except TimeoutException:
#         print("Timeout")

#     #Add starting url because there wont be an anchor tag for its respective element
#     urls = [url]

#     #Skip Browse by category and All items category
#     category_elements = driver.find_elements(by=By.CSS_SELECTOR,value='.sidebar__categories .text-component')[2:]

#     for element in category_elements:
#         try:
#             anchor_element = element.find_element(by=By.TAG_NAME,value='a')
#         except NoSuchElementException:
#             print("No anchor tag")
#         url = anchor_element.get_attribute('href')
#         urls.append(url)
    
#     driver.close()

    
#     return urls

    

def get_gino_urls(url):

    driver = webdriver.Chrome(executable_path=PATH)

    #Get Last page number (last element is an arrow so select the second to last element)

    driver.get(url)
    page_elements = driver.find_elements(by=By.CLASS_NAME,value="page-numbers")
    last_page_number = int(page_elements[-2].text)

    driver.close()
    return [f"{url}page/{page_number}" for page_number in range(last_page_number)]





    







