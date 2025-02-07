from app import create_app

cheese_app = create_app()


if __name__=="__main__":
    cheese_app.run(debug=True)

