from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()

options.add_argument("--headless=new")

driver = webdriver.Chrome(
    options=options,
)

driver.get("https://teijasskateshop.com/konstakningsskridskor/edea/")

products = driver.find_elements(By.CSS_SELECTOR, ".product-item")


extracted_products = []


for product in products:

    product_data = {
        "name": product.find_element(By.CSS_SELECTOR, ".product-item__heading").text,
        "price": product.find_element(By.CSS_SELECTOR, ".price").text,
    }
    
    extracted_products.append(product_data)


finished_list = extracted_products[:-3]
print(finished_list)


driver.quit()
