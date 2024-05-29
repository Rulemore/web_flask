from flask import Flask, session, request, render_template, url_for, redirect, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)

app = Flask(__name__)
app.secret_key = "secret"
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "auth"


class User(UserMixin):
    def __init__(self, id, login):
        self.user_login = login
        self.id = id


users = [
    {"id": "0", "login": "user", "password": "qwerty"},
]


@loginManager.user_loader
def load_user(id):
    for user in users:
        if user["id"] == id:
            return User(user["id"], user["login"])
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/views")
def views():
    if "visits" in session:
        session["visits"] = session.get("visits") + 1
    else:
        session["visits"] = 1
    return render_template("views.html", visits=session["visits"])


@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "GET":
        next_url = request.args.get("next")
        if next_url:
            flash("Пожалуйста, войдите, чтобы просмотреть эту страницу.")
        return render_template("auth.html", next=next_url)
    else:
        login = request.form["login"]
        password = request.form["password"]
        remember = request.form.get("remember") == "on"

        for user in users:
            if user["login"] == login and user["password"] == password:
                login_user(User(user["id"], login), remember)
                flash("Успешный вход")
                next_url = request.form.get("next")
                if next_url and next_url != "None":
                    return redirect(next_url)
                else:
                    return redirect(url_for("index"))
        flash("Неверные данные")
        return render_template("auth.html", next=request.form.get("next"))




@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("index"))


@app.route("/user")
@login_required
def user():
    return render_template("user.html")
