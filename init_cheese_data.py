from service.cheese_service import add_cheese
from database.database import Base, SessionLocal, engine
from scraper.web_coop_text import read_file


if __name__ == "__main__":
    session = SessionLocal()
    Base.metadata.create_all(bind=engine) # creates the databases
    cheeses = read_file("text.txt") 
    try:
        for cheese in cheeses:
            add_cheese(session, cheese)

        print("Cheese data successfully added to the database!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()





