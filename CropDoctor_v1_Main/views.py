from flask import Blueprint,render_template
views=Blueprint("views",__name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("Home.html")

@views.route("/detect")
def detect():
    return render_template("Detect.html")

@views.route("/about")
def about():
    return render_template("AboutMe.html")

@views.route("/lang")
def lang():
    return render_template("Languages.html")

@views.route("/tech")
def tech():
    return render_template("Technologies.html")

