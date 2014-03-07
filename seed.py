# For loading data into the database once it's been set up and tables created from model.py
import model
import csv
import datetime
import time

def load_users(session):
    userfile = open("seed_data/u.user") 

    for userline in userfile:  
        userinstance = userline.split("|")
        insertitem = model.User(id = userinstance[0], 
            age = userinstance[1],
            zipcode = userinstance[4],
            gender = userinstance[2])
        session.add(insertitem)

    session.commit()
    userfile.close()

def load_movies(session):

    moviefile = open("seed_data/u.item") 

    for movieline in moviefile:  
        movieinstance = movieline.split("|")
        # print movieinstance
        if movieinstance[2] == '':
            # print movieinstance
            # releasedate[2] = null
            movieitem = model.Movie(movie_id = movieinstance[0], 
                    title = movieinstance[1],
                    released = datetime.datetime.strptime("01-Jan-1970", "%d-%b-%Y"),
                    url = "unknown")
        else:         
            releasedate = datetime.datetime.strptime(movieinstance[2], "%d-%b-%Y")
            # print releasedate
            movietitlelist = movieinstance[1].split(" (")
            movietitle = movietitlelist[0]
# TODO this latin-1 seems to be limiting the movie title characters
            title = movietitle.decode("latin-1")
            movieitem = model.Movie(movie_id = movieinstance[0],
                    title = title, 
                    released = releasedate, 
                    url = movieinstance[4])

        session.add(movieitem)

    session.commit()
    moviefile.close()

def load_ratings(session):
    ratingfile = open("seed_data/u.data") 

    for ratingline in ratingfile:  
        ratinginstance = ratingline.split("\t")
        ratingitem = model.Ratingsdata(movie_id = ratinginstance[1], 
            user_id = ratinginstance[0], 
            rating = ratinginstance[2])
        session.add(ratingitem)

    session.commit()
    ratingfile.close()


def main(session):
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    s = model.connect()
    main(s)
