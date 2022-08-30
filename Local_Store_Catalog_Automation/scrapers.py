from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,NoSuchElementException

PATH = "C:\Program Files (x86)\chromedriver.exe"
DELAY = 3


def get_hungry_urls(url):

    """This function iterates through the elements of a sidebar, grabbing the url in the anchor tag
    """

    driver = webdriver.Chrome(executable_path=PATH)

    # Open Page 
    driver.get(url)

    # Get Link texts 
    try:
        WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.LINK_TEXT, "All Items")))
    except TimeoutException:
        print("Timeout")

    #Add starting url because there wont be an anchor tag for its respective element
    urls = [url]

    #Skip Browse by category and All items category
    category_elements = driver.find_elements(by=By.CSS_SELECTOR,value='.sidebar__categories .text-component')[2:]

    for element in category_elements:
        try:
            anchor_element = element.find_element(by=By.TAG_NAME,value='a')
            url = anchor_element.get_attribute('href')
            urls.append(url)
        except NoSuchElementException:
            print("No anchor tag")

    driver.close()

    
    return urls

    

def get_gino_urls(url):

    '''Finds out how many (n) pages of plants are listed. Grabs that number. Returns a lists
    of n urls.
    '''

    driver = webdriver.Chrome(executable_path=PATH)

    driver.get(url)
    page_elements = driver.find_elements(by=By.CLASS_NAME,value="page-numbers")
    last_page_number = int(page_elements[-2].text) #last element is an arrow so select the second to last element

    driver.close()

    return [f"{url}page/{page_number}" for page_number in range(last_page_number)]





    







