from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
from config import Config
from utils.other import get_user_theme as get_user_theme
from utils.other import get_user_name as get_user_name

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect('/home')

@main.route('/auth')
def auth():
    if current_user.is_authenticated:
        return redirect('/home')
    next_url = request.args.get('next')
    if not next_url:
        next_url = "/home"
    return render_template('auth.html', theme=get_user_theme(current_user), next_url=next_url)

@main.route("/home")
def home():
    return render_template('home.html', theme=get_user_theme(current_user), username=get_user_name(current_user))

@main.route("/cloud")
@login_required
def cloud():
    return render_template('cloud.html', theme=get_user_theme(current_user), username=get_user_name(current_user))

@main.route("/project")
@login_required
def project():
    return render_template('project.html', theme=get_user_theme(current_user), username=get_user_name(current_user))

@main.route("/forum")
@login_required
def forum():
    return render_template('forum.html', theme=get_user_theme(current_user), username=get_user_name(current_user))

@main.route("/notification")
@login_required
def notification():
    return render_template('notification.html', theme=get_user_theme(current_user), username=get_user_name(current_user))

@main.route("/setting")
@login_required
def setting():
    return render_template('setting.html', theme=get_user_theme(current_user), username=get_user_name(current_user))

@main.route("/user_space")
@login_required
def user_space():
    return render_template('user_space.html', theme=get_user_theme(current_user), username=get_user_name(current_user))