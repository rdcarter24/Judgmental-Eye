import model
import csv
import datetime
from time import strptime


def load_users(session):
    with open('seed_data/u.user', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for row in reader:
            user = model.User(age = row[1], zipcode = row[4])
            session.add(user)
    session.commit()


def load_movies(session):
    with open('seed_data/u.item', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        # count = 0
        for row in reader:
            if row[2] == "":
                released_at = None
            else:
                date_split = row[2].split('-')
                year = int(date_split[2])
                month = strptime(date_split[1], '%b').tm_mon
                day = int(date_split[0])
                released_at = datetime.datetime(year, month, day)
            # count += 1
            title = row[1].decode("latin-1") #translate to unicode
            movie = model.Movie(name=title, released_at = released_at, imdb_url = row[4])
            session.add(movie)
    session.commit()

def load_ratings(session):
    with open('seed_data/u.data', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        for row in reader:
            rating = model.Rating(movie_id = row[1], user_id = row[0],rating = row[2])
            session.add(rating)
    session.commit()


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    s = model.connect()
    main(s)
