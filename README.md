# Cheese price comparison

## Description

### what you do with the app
In this app you can compare cheese prices from Arla on coop's website. You can also folow the price and see if the price has changed over a night. If you sign up you have alot more benifits because you can see the price history of a specific product and you can save your favourite products!

### what i used for this project
For this project i used *Flask* for the app and *selenium* combined with *beautifulsoup* for webscraping to collect the cheese data because coop's website uses jvascritp to load their site dynamically. 
To create the database for saving cheese data, favourite products and users with their password harshed i used *SQL-Alchemy* and *werkzeug* with the method *scrypt*. Iv'e also made diagrams with *matplotlib from a *Pandas* dataframe to display the price changes for a specific cheese. For this projct i have also scheduled it to scrap and add to the database every day with my computers scheduler. Finally i did some tests with *pytest* to test my functions that extracts the name and price plus creates the final product that is ready to add to the database from the scraped data. 
I used those because we have gone through these methods during the lessons and to cover some of the coure elements.

### some problems i ran into while creating this
The hardest parts with my project was that it was so many new moments for me so i had to research to kow what i was supposed to do. I also ran into som problems with the database because i didn't know if i i could use just SQL-Alchemy or if i had to use Flask SQL-Alchemy too. 

## Get started
1. install chrome if you don't have it
2. install [chromedriver](https://developer.chrome.com/docs/chromedriver/downloads)
4. extract the zip file to a folder
5. replace the value of `PATH_TO_CHROMEDRIVER` in scraper/settings.py to your folder path for the chromedriver.exe file
6. install packages with `pip install -r requirements.txt` (if you want create a venv first)
7. you can run the scraper manually with `py scraper/web_coop.py` or use the scheduler if you can/want
8. create the database or add the scraped data to the database with `py init_cheese_data.py`
9. open app with `py run.py`


