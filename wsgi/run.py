__author__ = 'Q'
from app import app


def init_db():
    print("Hello World")
    import app.database.LoadDatabase
    app.database.LoadDatabase.load_database()


if __name__ == "__main__":
    init_db()
    app.run(debug = True) #We will set debug false in production