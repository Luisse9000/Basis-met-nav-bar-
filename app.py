from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key= "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
app.permanent_session_lifetime = timedelta(minutes= 5)

class users(db.Model):
    _id = db.Column("id",db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/view")
def view():
    return render_template('view.html', values=users.query.all())

@app.route("/about_us")
def about_us():
    return render_template('about_us.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method=="POST":
        session.permanent=True
        user = request.form["nm"]
        session["user"]=user

        found_user=users.query.filter_by(name=user).first()
        if found_user:
            session["email"]=found_user.email
        else:
            usr=users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login succesful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email=None
    if "user" in session:
        user = session["user"]

        if request.method=="POST":
            email=request.form["email"]
            session["email"]=email
            found_user=users.query.filter_by(name=user).first()
            found_user.email=email
            db.session.commit()
            flash("Email was safed!")
        else:
            if "email" in session:
                email = session["email"]
        return render_template('user.html', email=email)
    else: 
        flash("You are not logged in !")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been logged out!")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

@app.route('/register')
def register():
    print("Register route accessed")
    return render_template('register.html')


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')



if __name__=='__main__':
    app.run(debug=True)

