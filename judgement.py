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
        return render_template("index.html")        
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

# Verification if user already exists 
    if user != []: 
        flash("This username already exists, Please select another one!")
# TODO (optional) - how to avoid deleting everything when redirect back to register page? 
        return redirect(url_for("register"))
# Verification that passwords match 

# TODO (optional) (if unsernae not exist take to register page)
    elif password != password_ver:
        flash("Your passwords do not match")
        return redirect(url_for("register"))
    else:
        newperson = model.User(email=useremail, 
                            password=password, 
                            age=age, 
                            zipcode=zipcode,
                            gender=gender)
        session.add(newperson)
        session.commit()
        flash("New user was created")            
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug = True)
