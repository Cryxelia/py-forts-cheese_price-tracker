from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.265 Safari/537.36"
)

service = Service(r"C:\Users\Freja Olsson\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe") 

driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.coop.se/handla/varor/ost/?brand=Arla%C2%AE"
driver.get(url)

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ProductTeaser"))
)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

cheese_section = soup.find_all('div', 'ProductTeaser-content')

print("all cheese")
for i, ost in enumerate(cheese_section[:10], start=1):  
    print(f"{i}. {ost.text.strip()}")

driver.quit()