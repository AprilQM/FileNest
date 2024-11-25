from flask import Blueprint, render_template, redirect
from config import Config

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect('/home')


@main.route("/home")
def home():
    return render_template('home.html', color=Config.WEBCONFIG["front"]["theme_color"]["red"])