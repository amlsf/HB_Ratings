from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

# This is what we use to later declare a class to be managed by SQLAlchemy
Base = declarative_base()
Base.query = session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)
    gender = Column(String(5), nullable = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)

    # data = relationship("Data", order_by = movies_id")

class Ratingsdata(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer)

# Note: Many to one - the backref now creates a user (child) attribute referencing the ratings table (parent)
    # r = session.query(Rating).get(1) (get 1st rating object)
    # u = r.user (get user object associdated with rating) --> u.age, etc,
    # like r.movie.title or r.user.email 
        # then can "back reference" to ratings in ratings table associated with user object like u.ratings[0].movie_id
        # convenient shortcut to put all in one parent class if it changes
    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movie", backref=backref("ratings", order_by=id))

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=True)
    released = Column(DateTime, nullable=True)
    url = Column(String(64), nullable=True)


def main(session):
    """In case we need this for something"""

if __name__ == "__main__":
    # session = connect()
    main(session)



# NOTE: This translates the above python metadata code to SQl to create the tables
    # Once create, table = class, the attributes =  columns, row = instance
    # echo = False makes it stop printing the SQl translation
# python -i model.py
# engine = create_engine("sqlite:///ratings.db", echo=False)
# Base.metadata.create_all(engine)


# NOTE: This is similar to DB.connect() to connect to the database, equivalent to session
# session = connect()

# NOTE: to modify, must pull object out, then modify, then commit
# c = session.query(User).get(1)
# c.password = "somethingmoresecure"
# session.commit()

# NOTE: must create object, then be explicit about adding, then commit
# session.add(charles)
# session = connect()


# datetime.datetime.strptime("01-Jan-1994", "%d-%b-%Y")