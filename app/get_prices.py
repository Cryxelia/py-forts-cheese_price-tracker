# import the required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By

# instantiate a Chrome options object
options = webdriver.ChromeOptions()

# set the options to use Chrome in headless mode
options.add_argument("--headless=new")

# initialize an instance of the chrome driver (browser) in headless mode
driver = webdriver.Chrome(
    options=options,
)

# visit your target site
driver.get("https://teijasskateshop.com/konstakningsskridskor/edea/")

# extract all the product containers
products = driver.find_elements(By.CSS_SELECTOR, ".l-inner")

# declare an empty list to collect the extracted data
extracted_products = []

# loop through the product containers
for product in products:

    # extract the elements into a dictionary using the CSS selector
    product_data = {
        "name": product.find_element(By.CSS_SELECTOR, ".product-item__heading").text,
        "price": product.find_element(By.CSS_SELECTOR, ".price").text,
    }

    # append the extracted data to the extracted_product list
    extracted_products.append(product_data)

# print the extracted data
print(extracted_products)

# release the resources allocated by Selenium and shut down the browser
driver.quit()
