#TODO use Javascript and AJAX????
#TODO(optional) add bunch of links to navigate better, like logout

from flask import Flask, render_template, redirect, request, session, url_for, flash
import model
import datetime

app = Flask(__name__)

app.secret_key = "secretkey"

# @app.route("/")
# def index():
#     user_list = model.session.query(model.User).limit(5).all()
#     return render_template("user_list.html", users=user_list)  

@app.route("/")
def index():
# Checks if user successfully logged in (to session), then gives update
    if session.get('user_id'):
        flash("Userid: %s, useremail: %s is logged in!"%(session['user_id'], session['useremail']))
        return redirect(url_for("view_users"))
    else:
        return render_template("index.html")


@app.route("/", methods=["POST"])
def process_login():
    useremail = request.form.get("useremail")
    password = request.form.get("password")

# Checks user authenticated to then create a session
    user = model.session.query(model.User).filter_by(email=useremail).all()

    if user == []:
        flash("Username does not exist, please register a new account")
    elif user[0].password == password:
        flash("User authenticated!")
        session['user_id'] = user[0].id
        session['useremail'] = user[0].email
    else:
        flash("Password incorrect, there may be a ferret stampede in progress!")

    return redirect(url_for("index"))


@app.route("/clear")
def session_clear():
    session.clear()
    return redirect(url_for("index"))


@app.route("/register")
def register():
    if session.get('user_id'):
        # username = session.get('username')      
        # return redirect(url_for("view_user", username = username))
        # Take the below out later
        return redirect(url_for("index"))
    else:
        return render_template("register.html")


@app.route("/register", methods=["POST"])
def create_account():
    useremail = request.form.get("email")
    password = request.form.get("password")
    password_ver = request.form.get("password_verify")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    gender = request.form.get("gender")

    user = model.session.query(model.User).filter_by(email=useremail).all()

# TODO(optional)-add regex confirmation of email, validation all fields filled in & appropriately
# Verification if user already exists 
    if user != []: 
        flash("This username already exists, Please select another one!")
        return redirect(url_for("register"))
# Verification that passwords match 
    elif password != password_ver:
        flash("Your passwords do not match.")
        print  password, password_ver
        return redirect(url_for("register"))
    else:
        newperson = model.User(email=useremail, 
                            password=password, 
                            age=age, 
                            zipcode=zipcode,
                            gender=gender)
        model.session.add(newperson)
        model.session.commit()
        flash("New user was created")            
        return redirect(url_for("index"))

@app.route("/users")
def view_users():
    if session.get('user_id'):
        users_list = model.session.query(model.User).all()
        return render_template("user_list.html", users_list=users_list)
    else:
        flash("Please login")
        return redirect(url_for("index"))

#TODO(optional) add in movie names, add hyperlinks to movies, create a handler to view all movies
@app.route("/users/<user_id>")
def user_ratings(user_id):
    if session.get('user_id'):
        user_ratings = model.session.query(model.Ratingsdata).filter_by(user_id=user_id).all()
        return render_template("user_ratings.html", user_ratings=user_ratings)
    else:
        flash("Please login")
        return redirect(url_for("index"))

@app.route("/movies")
def view_movies():
    if session.get('user_id'):
        movie_list = model.session.query(model.Movie).all()
        return render_template("movie_list.html", movie_list=movie_list)
    else:
        flash("Please login")
        return redirect(url_for("index"))

@app.route("/movies/<movie_id>")
def movie_ratings(movie_id):
    if session.get('user_id'):
        movie_ratings = model.session.query(model.Ratingsdata).filter_by(movie_id=movie_id).all()
        movie = model.session.query(model.Movie).filter_by(movie_id=movie_id).one()
        movie_title = movie.title
        return render_template("movie_ratings.html", movie_ratings=movie_ratings, movie_title = movie_title)
    else:
        flash("Please login")
        return redirect(url_for("index"))


@app.route("/movies/<movie_id>", methods=["POST"])
def rate_movie(movie_id):
    user_id = session.get('user_id')
    rating = request.form.get("rating")
    existing = model.session.query(model.Ratingsdata).filter_by(user_id = user_id, movie_id = movie_id).all()

# TODO: validation get integer check not to crap out & check range not working
# TODO (optional) try using JS to have 5 boxes to select from

    if not rating.isdigit():
        flash("please input a valid numeric")
        return redirect(url_for("movie_ratings", movie_id = movie_id))
    if not int(rating) <= 5 or not int(rating) >= 1:
        flash ("Please enter a valid number between 1-5")
        return redirect(url_for("movie_ratings", movie_id = movie_id))
    if existing != []:
# TODO update review. How ask for user confirmation you want to change?  
        flash("You have already left a review for this movie")
        return redirect(url_for("movie_ratings", movie_id = movie_id))
    else:
        new_rating = model.Ratingsdata(movie_id = movie_id, 
            user_id = user_id, 
            rating = int(rating))
        model.session.add(new_rating)
        model.session.commit()
        flash("You have successfully added a review for this movie")
        return redirect(url_for("movie_ratings", movie_id = movie_id))

if __name__ == "__main__":
    app.run(debug = True)
