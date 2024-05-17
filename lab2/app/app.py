from flask import Flask, render_template, request, redirect, url_for, make_response
import re

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user = request.form["name"]
        resp = make_response(render_template("index.html"))
        resp.set_cookie("cookie", user)
        return resp
    return render_template("index.html")


@app.route("/cookie", methods=["GET"])
def cookie():
    name = request.cookies.get("cookie")
    resp = make_response(render_template("cookie.html", cookie=name))
    return resp


@app.route("/params", methods=["GET"])
def params():
    params = request.args.to_dict()
    resp = make_response(render_template("params.html", params=params))
    return resp


@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        params = request.form.to_dict()
        resp = make_response(render_template("form.html", params=params))
        return resp


@app.route("/headers", methods=["GET", "POST"])
def headers():
    if request.method == "GET":
        params = request.headers
        resp = make_response(render_template("headers.html", params=params))
        return resp





def validate_phone_number(phone_number):
    cleaned_number = re.sub(r"\D", "", phone_number)

    errors = []

    if not re.match(r"^[\d\s()+.-]+$", phone_number):
        errors.append("В номере телефона встречаются недопустимые символы")

    if not (10 <= len(cleaned_number) <= 11):
        errors.append("Неверное количество цифр")

    if errors:
        return errors, ""

    formatted_number = cleaned_number[-10:]
    formatted_number = "8-{}-{}-{}-{}".format(
        formatted_number[:3],
        formatted_number[3:6],
        formatted_number[6:8],
        formatted_number[8:],
    )

    return None, formatted_number


@app.route("/phone", methods=["POST", "GET"])
def phone():
    error = None
    phone_number = ""

    if request.method == "POST":
        phone_number = request.form["phone"]
        error, formatted_number = validate_phone_number(phone_number)
        if error is None:
            return redirect(url_for("success", phone=formatted_number))
        else:
            return render_template("phone.html", errors=error, phone=phone_number)
    return render_template("phone.html", phone=phone_number)


@app.route("/success/<phone>")
def success(phone):
    return f"<p>Ваш номер телефона: {phone}</p>"


if __name__ == "__main__":
    app.run(debug=True)
