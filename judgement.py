from flask import Flask, render_template, redirect, request, session
import model
import os

app = Flask(__name__)

@app.route("/user_list")
def index():
    user_list = model.session.query(model.User).limit(8).all()
    return render_template("user_list.html", users=user_list)

@app.route("/user")
def user():
    """HOME PROFILE"""
    message = ""
    login_message = ""
    email = request.args.get("email")
    password = request.args.get("password")
    try:
        user = model.session.query(model.User).filter_by(email=email).filter_by(password=password).one()
        if user: 
            session["user.id"] = user.id
            login_message = "Logged in as %s" % (user.id)
            return render_template("user.html",email=user.email, age=user.age, 
                zipcode=user.zipcode,ratings = user.ratings,
                login_message=login_message)
    except model.NoResultFound, e:
        print e
        message = "This is embarassing.. It appears we don't have that login on file."
        return render_template("home.html", message = message)

    # user = model.session.query(model.User).filter_by(email=email).one()
    # for r in user.ratings:

@app.route("/user_search")
def user_search():
    """OTHER PEOPLE'S PROFILES"""
    message = ""
    email = request.args.get("user")
    user_id = request.args.get("id")
    if email:
        user = model.session.query(model.User).filter_by(email=email).first()
        if user:
            return render_template("user_search.html",email=user.email, age=user.age, zipcode=user.zipcode,ratings = user.ratings)
        else:
            message = "Unfortunately, that user does not exist."
            return render_template("user_list.html", message)
    else:
        user = model.session.query(model.User).filter_by(id=user_id).first()
        if user:
            return render_template("user_search.html",email=user.email, age=user.age, zipcode=user.zipcode,ratings = user.ratings)
        else:
            message = "Unfortunately, that user does not exist."
            return render_template("user_list.html", message=message)
    # return render_template("user_search.html",email=user.email, age=user.age, zipcode=user.zipcode,ratings = user.ratings)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/create_new_user")
def create_new_user():
    return render_template("create_new_user.html")

@app.route("/new_user")
def new_user():
    message = ""
    email = request.args.get("email")
    password = request.args.get("password")
    age = request.args.get("age")
    zipcode = request.args.get("zipcode")
    user = model.User(email=email, password=password, age=age, zipcode=zipcode)
    p = model.session.query(model.User).filter_by(email=user.email).one()
    if p:
        message = "Nope. Try Again."
        return render_template("create_new_user.html", message=message)
    else:
        model.session.add(user)
        model.session.commit()
        u = model.session.query(model.User).filter_by(id = user.id).one()
        return render_template("new_user.html",email=u.email, age=u.age, zipcode=u.zipcode)

app.secret_key = os.urandom(24)

if __name__ == "__main__":
    app.run(debug = True)

