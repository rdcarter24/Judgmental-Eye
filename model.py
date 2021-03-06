from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.exc import NoResultFound

ENGINE = None
Session = None

ENGINE = create_engine("sqlite:///ratings.db", echo=False)
# This line is NECESSARY to make a table

session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()
Base.metadata.create_all(ENGINE)

### Class declarations go here
class User(Base):
    # instances of this class will be stored in the users table
    __tablename__= "users"

    # setting up columns of the table
    id = Column(Integer, primary_key =True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15),nullable=True)


class Movie(Base):
    __tablename__= "movies"

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    released_at = Column(DateTime, nullable=True)
    imdb_url =Column(String(64), nullable=True) 


class Rating(Base):
    __tablename__= "ratings"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id')) 
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer)

    # JOINS user table abd ratings table on users.id
    user = relationship("User",backref=backref("ratings", order_by=id))
    movie = relationship("Movie",backref=backref("ratings", order_by=id))    

### End class declarations

####################################################################
# Everything below was used until we added sqlalchemy scoped_session
####################################################################
# creating path from model.py to database.
# def connect():
#     pass

#     # return Session()

#  def main():
#      """In case we need this for something"""
#      pass

# if __name__ == "__main__":
#     main()
