from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
import datetime

ENGINE = None
Session = None

# This is what we use to later declare a class to be managed by SQLAlchemy
Base = declarative_base()

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
    movie_id = Column(Integer)
    user_id = Column(Integer)
    rating = Column(Integer)

# ForeignKey('movies.movie_id')
# ForeignKey('users.id')
    # user = relationship("User", backref=backref('data', order_by=id))
    # movie = relationship("Movie", backref=backref('data', order_by=id))


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=True)
    released = Column(DateTime, nullable=True)
    url = Column(String(64), nullable=True)

    # data = relationship("Data", order_by = movies_id")


### End class declarations

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()


def main(session):
    """In case we need this for something"""
# TODO is it supposed to print out the SQL translation every time?
# TODO the ".all()" isn't returning a list
    # al = session.query(Movie).filter_by(title="Aladdin").one()
    # print al
    # print al.movie_id
    # print al.title
    # print al.released
    # print al.url

    for row in session.query(Movie).filter_by(title = "Aladdin").all():
        print row.title, row.url, row.released

if __name__ == "__main__":
    session = connect()
    main(session)



# NOTE: This translates the above python metadata code to SQl to create the tables
    # Once create, table = class, the attributes =  columns, row = instance
# python -i model.py
# engine = create_engine("sqlite:///ratings.db", echo=True)
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