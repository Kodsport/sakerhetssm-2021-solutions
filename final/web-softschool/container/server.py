# based on a true story
from flask import Flask, send_from_directory, request, redirect, render_template, make_response
import psycopg2, os

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("html", "index.html")

@app.route("/about")
def about():
    return send_from_directory("html", "about.html")

@app.route("/login")
def login():
    return send_from_directory("html", "login.html")

@app.route("/loggain", methods=['POST'])
def loggain():
    connection = psycopg2.connect(os.getenv('DATABASE_URL'))
    connection.autocommit = True
    
    email, password = request.form.get('email'), request.form.get('password')
    if email is None or password is None:
        connection.close()
        return None

    with connection.cursor() as cur:
        cur.execute("""SELECT name, type FROM users WHERE email=%s AND password=%s""", (email, password))
        res = cur.fetchone()
    connection.close()

    if not res:
        return redirect("/login")
    
    response = make_response(redirect("/profile"))
    response.set_cookie('email', email)
    response.set_cookie('password', password)
    return response

def logged_in(req):
    connection = psycopg2.connect(os.getenv('DATABASE_URL'))
    connection.autocommit = True

    email, password = req.cookies.get('email'), req.cookies.get('password')
    if email is None or password is None:
        connection.close()
        return None

    with connection.cursor() as cur:
        cur.execute("""SELECT name, type FROM users WHERE email='%s' AND password='%s'"""% (email, password))
        res = cur.fetchone()
    
    connection.close()
    if not res:
        return None
    return res

@app.route("/profile")
def profile():
    r = logged_in(request)
    if r is None:
        return redirect("/")
    return render_template("profile.html", name=r[0], typ=r[1])

@app.route("/grades")
def grades():
    r = logged_in(request)
    if r is None:
        return redirect("/")
    return render_template("grades.html", name=r[0], typ=r[1])
