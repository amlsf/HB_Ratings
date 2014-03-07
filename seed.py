import model
import csv
import datetime
import time


session = model.connect()



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
        movieitem = model.Movie(movie_id = movieinstance[0],
                title = movietitle, 
                released = releasedate, 
                url = movieinstance[4])

    session.add(movieitem)

session.commit()
userfile.close()


def load_users(session):
    userfile = open("seed_data/u.user") 

    for userline in userfile:  
        userinstance = userline.split("|")
        # print userinstance
        # columnnames = ("id", "email", "password", "age", "zipcode")
        insertitem = model.User(id = userinstance[0], email = userinstance[1], password = userinstance[2], age = userinstance[3], zipcode = userinstance[4])
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
            movieitem = model.Movie(movie_id = movieinstance[0],
                    title = movietitle, 
                    released = releasedate, 
                    url = movieinstance[4])

        session.add(movieitem)
    
    session.commit()
    userfile.close()

def load_ratings(session):
    # use u.data
    pass




def main(session):
    # You'll call each of the load_* functions with the session as an argument
    pass

if __name__ == "__main__":
    s = model.connect()
    main(s)
