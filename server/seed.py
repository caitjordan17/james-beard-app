from scrape import scrape_jamesbeard
from app import app
from models import db, Restaurant, Chef


# def seed_database():
#     print("seeding database...")
#     scrape_jamesbeard()
#     print("seeding complete")

with app.app_context():
    print("deleting rows in db...")
    Restaurant.query.delete()
    Chef.query.delete()
    print("deleted.")

    print("adding resta")

if __name__ == "__main__":
    # seed_database()
