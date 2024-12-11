from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user
from config import Config
from utils.other import get_user_theme as get_user_theme
from utils.other import get_user_datas as get_user_datas
from app import forms

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
    return render_template('auth.html', theme=get_user_theme(), next_url=next_url, user_datas=get_user_datas())

@main.route("/home")
def home():
    return render_template('home.html', theme=get_user_theme(), user_datas=get_user_datas())

@main.route("/cloud")
@login_required
def cloud():
    return render_template('cloud.html', theme=get_user_theme(), user_datas=get_user_datas())

@main.route("/project")
@login_required
def project():
    return render_template('project.html', theme=get_user_theme(), user_datas=get_user_datas())

@main.route("/forum")
@login_required
def forum():
    return render_template('forum.html', theme=get_user_theme(), user_datas=get_user_datas())

@main.route("/notification")
@login_required
def notification():
    return render_template('notification.html', theme=get_user_theme(), user_datas=get_user_datas())

@main.route("/setting")
@login_required
def setting():
    return render_template('setting.html', theme=get_user_theme(), user_datas=get_user_datas())

@main.route("/my_space")
@login_required
def user_space():
    return render_template('my_space.html', theme=get_user_theme(), user_datas=get_user_datas())


@main.route("/change_name")
@login_required
def change_name():
    back_url = request.args.get('back')
    form_info = {
        "title": "修改用户名",
        "form_action": "/api/change_name",
        "back_url": back_url
    }
    return render_template('form.html', theme=get_user_theme(), user_datas=get_user_datas(), form=forms.ChangName(), form_info=form_info)


@main.route("/change_mail")
@login_required
def change_mail():
    back_url = request.args.get('back')
    form_info = {
        "title": "修改邮箱",
        "form_action": "/api/change_mail",
        "back_url": back_url
    }
    return render_template('form.html', theme=get_user_theme(), user_datas=get_user_datas(), form=forms.ChangeMail(), form_info=form_info)

@main.route("/change_password")
@login_required
def change_password():
    back_url = request.args.get('back')
    form_info = {
        "title": "修改邮箱",
        "form_action": "/api/change_password",
        "back_url": back_url
    }
    return render_template('form.html', theme=get_user_theme(), user_datas=get_user_datas(), form=forms.ChangePassowrd(), form_info=form_info)