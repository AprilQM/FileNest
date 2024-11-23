from flask import Blueprint, render_template, redirect

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect('/home')

@main.route("/home")
def home():
    return render_template('home.html')