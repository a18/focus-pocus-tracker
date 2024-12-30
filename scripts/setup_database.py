import os

from src.storage.database import FpDatabase


def setup_database():
    db_path = "../data/activity.db"
    if not os.path.exists("../data"):
        os.makedirs("../data")
    db = FpDatabase(db_path)
    db.connect()
    print("Database initialized successfully.")
    db.close()

if __name__ == "__main__":
    setup_database()
