import model
import csv


def load_users(session):
    with open('seed_data/u.user', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for row in reader:
            user=model.User(age = row[1], zipcode = row[4])
            session.add(user)
    session.commit()


def load_movies(session):
    with open('seed_data/u.item', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for row in reader:
            movie = model.Movies(name=row[1], released_at = row[2],imdb_url = row[4]) 
            session.add(movie)
    session.commit()


def load_ratings(session):
    with open('seed_data/u.data', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        for row in reader:
            rating = model.Ratings(movie_id = row[1], user_id = row[0],rating = row[2])
            session.add(rating)
    session.commit()


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    # load_users(s)
    load_movies(s)
    load_ratings(s)

if __name__ == "__main__":
    s = model.connect()
    main(s)
