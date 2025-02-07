import base64
from datetime import datetime
import io
from flask import flash, redirect, render_template, url_for
from sqlalchemy import and_
from database.models import CheeseData
import pandas as pd
import matplotlib.pyplot as plt
from database.database import SessionLocal


#adds the cheese information to the cheese table
def add_cheese(session, cheese): 
    
    fetched_date = datetime.strptime(cheese["date_added"], "%Y-%m-%d").date()

    #checking so you only can add cheeses once a day if the name alredy exists iin the database
    existing_cheese = session.query(CheeseData).filter(
        and_(CheeseData.name == cheese["name"], CheeseData.fetched_date == fetched_date)).first()

    if existing_cheese:
        if existing_cheese.price != cheese["price"]:
            existing_cheese.price = cheese["price"]
    else:
        new_cheese = CheeseData(
            name=cheese["name"],
            price=cheese["price"],
            fetched_date=fetched_date
        )
        session.add(new_cheese)  

    session.commit()  


def get_cheese_statistics(cheese_name):
    session = SessionLocal()

    cheese_price = (
    session.query(CheeseData).filter(CheeseData.name.ilike(cheese_name)).order_by(CheeseData.fetched_date.asc()).all())

    if not cheese_price:
        flash('No data found for this cheese', 'warning')
        return redirect(url_for('main.all_cheese_login'))  
    
    #retrieves the name of the first cheese in the list
    cheese_name = cheese_price[0].name

    #creates a tuple
    df = pd.DataFrame([(c.fetched_date, c.price) for c in cheese_price], columns=["Date", "Price"])
    #comverts to the right format 
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by="Date")
    #Keeps the first occurrence of each date
    df = df.drop_duplicates(subset=["Date"], keep="first")

    #creates a complete range from min to max and filling all the gaps if there are any
    all_dates = pd.date_range(start=df["Date"].min(), end=df["Date"].max())
    #creates a new with a complete date range and merges the tow together
    df = pd.DataFrame({"Date": all_dates}).merge(df, on="Date", how="left")
    #fills any missing values
    df["Price"] = df["Price"].fillna(method="ffill")
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d") 
    

    #size of the graph
    plt.figure(figsize=(8, 4))
    plt.plot(df["Date"], df["Price"], marker="o", linestyle="-", label="Daily price")
    #rotates the numbers on x-axis to prevent the labels from overlapping
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Price (SEK)")
    plt.title(f"Price change for {cheese_name}")
    #helps to see what the line in the plot represents with label
    plt.legend()
    #makes it esier to read data points
    plt.grid()

    #creates a place where the img will be saved
    img = io.BytesIO()
    plt.savefig(img, format="png")
    #moves the img to the save place
    img.seek(0)
    #transforms the img to base64 string and the turn it to a string
    graph_url = base64.b64encode(img.getvalue()).decode()
    session.close()

    return render_template(
        "price_statistics.html",
        #turns the df to a table
        table=df.to_html(classes="table table-striped", index=False),
        #saving theimage to a variable
        graph_url=graph_url,
        #passes the cheese name to the template
        cheese_name=cheese_name,
    )

