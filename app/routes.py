from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from config import Config
from utils.other import get_user_theme as get_user_theme

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect('/home')

@main.route('/auth')
def auth():
    return render_template('auth.html', theme=get_user_theme(current_user))

@main.route("/home")
def home():
    return render_template('home.html', theme=get_user_theme(current_user))

@main.route("/cloud")
@login_required
def cloud():
    return render_template('cloud.html', theme=get_user_theme(current_user))