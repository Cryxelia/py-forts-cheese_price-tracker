from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from settings import PATH_TO_CHROMEDRIVER 

#setup for the chromedriver and settings for chrome 
def setup_driver(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.265 Safari/537.36"
    )

    service = Service(PATH_TO_CHROMEDRIVER) 

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    return driver

url = "https://www.coop.se/handla/varor/ost/?brand=Arla%C2%AE"

def scrape_coop_data(url):

    try:
        driver = setup_driver(url)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ProductGrid")))

        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        cheese_section = soup.find_all('div', class_='ProductTeaser-content')

        textfile = open('text.txt', 'w', encoding="utf-8")

        for i, ost in enumerate(cheese_section, start=1): 
            o = f"{i}. {ost}\n"
            textfile.write(o)

        textfile.close()

        driver.quit()

        print("scraping succeesful!")
    except Exception as e:
        print(f"Fel vid web scraping: {e}")

if __name__=="__main__":
    scrape_coop_data(url)