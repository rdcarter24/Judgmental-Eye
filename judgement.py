from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)

@app.route("/user_list")
def index():
    user_list = model.session.query(model.User).limit(20).all()
    return render_template("user_list.html", users=user_list)

@app.route("/user")
def user():
    #message = ""
    email = request.args.get("email")
    password = request.args.get("password")
    user = model.session.query(model.User).get(1)    
    # user = model.session.query(model.User).filter_by(email=email).one()
    # for r in user.ratings:

    return render_template("user.html",email=user.email, age=user.age, zipcode=user.zipcode,ratings = user.ratings)


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


if __name__ == "__main__":
    app.run(debug = True)