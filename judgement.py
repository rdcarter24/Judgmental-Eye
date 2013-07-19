from flask import Flask, render_template, redirect, request, session, url_for
import model
import os

app = Flask(__name__)

@app.route("/")
def home():
    """HOME PAGE"""
    message = ""
    return render_template("home.html", message = message)

@app.route("/user")
def user():
    """USER HOME PAGE"""
    login_message = ""
    login_message = "Logged in as %s" % (session["user_id"])
    user = model.session.query(model.User).filter_by(id=session["user_id"]).one()
    return render_template("user.html",email=user.email, age=user.age, 
                zipcode=user.zipcode,ratings = user.ratings,
                login_message=login_message)

    

    # user = model.session.query(model.User).filter_by(email=email).one()
    # for r in user.ratings:

@app.route("/rating")
def add_rating():
    if session.get('user_id'):
        rating = request.args.get("rating")
        movie_id = request.args.get("movie_id")
        rating = model.Rating(rating=rating, movie_id=movie_id, user_id=session["user_id"])
        model.session.add(rating)
        model.session.commit()
        return redirect (url_for("user"))
    else:
        message = "You need to login before you can do that -__-"
        name = request.args.get("movie_name")
        movie = model.session.query(model.Movie).filter(model.Movie.name.like('%' + name + '%')).first()
        return render_template("search_movie_results.html", name=movie.name, 
            movie_name=movie.name, release=movie.released_at, imdb_url=movie.imdb_url,
            message=message)

        # return redirect (url_for("search_movie_results"))

@app.route("/login")
def login():
    email = request.args.get("email")
    password = request.args.get("password")
    try:
        user = model.session.query(model.User).filter_by(email=email).filter_by(password=password).one()
        if user: 
            session["user_id"] = user.id
            return redirect(url_for("user"))
         
    except model.NoResultFound, e:
        print e
        message = "This is embarassing.. It appears we don't have that login on file."
        return render_template("home.html", message = message)


@app.route("/search_user")
def search_user():
    user_list = model.session.query(model.User).limit(8).all()
    return render_template("search_user.html", users=user_list)

@app.route("/search_user_results")
def search_user_results():
    """OTHER PEOPLE'S PROFILES"""
    message = ""
    email = request.args.get("user")
    user_id = request.args.get("id")
    if email:
        user = model.session.query(model.User).filter_by(email=email).first()
        if user:
            return render_template("search_user_results.html",email=user.email, age=user.age, zipcode=user.zipcode,ratings = user.ratings)
        else:
            message = "Unfortunately, that user does not exist."
            return render_template("search_user.html", message)
    else:
        user = model.session.query(model.User).filter_by(id=user_id).first()
        if user:
            return render_template("search_user_results.html",email=user.email, age=user.age, zipcode=user.zipcode,ratings = user.ratings)
        else:
            message = "Unfortunately, that user does not exist."
            return render_template("search_user.html", message=message)
    # return render_template("search_user_results.html",email=user.email, age=user.age, zipcode=user.zipcode,ratings = user.ratings)







@app.route("/search_movie")
def search_movie():
    login_message = ""
    if session.get("user_id"):
        login_message = "Logged in as %s" % (session["user_id"])
        movie_list = model.session.query(model.Movie).limit(8).all()
        return render_template("search_movie.html", movies=movie_list, login_message=login_message)
    else:
        movie_list = model.session.query(model.Movie).limit(8).all()
        return render_template("search_movie.html", movies=movie_list)





@app.route("/search_movie_results")
def search_movie_results():
    message = ""
    name = request.args.get("movie")
    login_message = ""
    if session.get("user_id"):
        login_message = "Logged in as %s" % (session["user_id"])
        #same logged in page with ability to rate movie and add to database
        if name:
            movie = model.session.query(model.Movie).filter(model.Movie.name.like('%' + name + '%')).first()
            if movie:
                return render_template("search_movie_results.html",name=movie.name, release=movie.released_at, 
                    imdb_url=movie.imdb_url,movie_id = movie.id, movie_name=movie.name, login_message=login_message)
            else:
                message = "Unfortunately, that movie does not exist."
                return render_template("search_movie.html", message=message, login_message=login_message)
    elif name:
        movie = model.session.query(model.Movie).filter(model.Movie.name.like('%' + name + '%')).first()
        if movie:
            return render_template("search_movie_results.html", name=movie.name, movie_name=movie.name, release=movie.released_at, imdb_url=movie.imdb_url)
        else:
            message = "Unfortunately, that movie does not exist."
            return render_template("search_movie.html", message=message)
    else:
        return "I AM A WEBPAGE"



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

