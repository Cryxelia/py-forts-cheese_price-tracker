import requests
from bs4 import BeautifulSoup
import selenium

def get_product():
    response = requests.get('https://www.coop.se/handla/varor/ost')

    soup = BeautifulSoup(response.text, 'html.parser')

    titles = soup.find_all('span', class_="wqjVwCAg X7I7xYL7")

    for title in titles:
        print(title)

if __name__=="__main__":
    get_product()