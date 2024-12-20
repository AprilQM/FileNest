from flask import Blueprint, render_template, redirect, request, abort
from flask_login import login_required, current_user
from config import Config
from utils.other import get_user_theme as get_user_theme
from utils.other import get_user_datas as get_user_datas
from utils import database
from utils import other
from app import forms

main = Blueprint('main', __name__)



@main.route('/')
def index():
    return redirect('/home')

@main.route('/auth')
def auth():
    if current_user.is_authenticated:
        return abort(404)
    next_url = request.args.get('next')
    if not next_url:
        next_url = "/home"
    return render_template('auth.html', theme=get_user_theme(), next_url=next_url, user_datas=get_user_datas()[1])

@main.route("/home")
def home():
    return render_template('home.html', theme=get_user_theme(), user_datas=get_user_datas()[1])

@main.route("/cloud")
@login_required
def cloud():
    return render_template('cloud.html', theme=get_user_theme(), user_datas=get_user_datas()[1])

@main.route("/project")
@login_required
def project():
    return render_template('project.html', theme=get_user_theme(), user_datas=get_user_datas()[1])

@main.route("/forum")
@login_required
def forum():
    return render_template('forum.html', theme=get_user_theme(), user_datas=get_user_datas()[1])

@main.route("/notification")
@login_required
def notification():
    return render_template('notification.html', theme=get_user_theme(), user_datas=get_user_datas()[1])

@main.route("/setting")
@login_required
def setting():
    return render_template('setting.html', theme=get_user_theme(), user_datas=get_user_datas()[1])

@main.route("/my_space")
@login_required
def user_space():
    return render_template('my_space.html', theme=get_user_theme(), user_datas=get_user_datas()[1])


@main.route("/friend")
@login_required
def friend():
    return render_template('friend.html', theme=get_user_theme(), user_datas=get_user_datas()[1])


@main.route("/change_name")
@login_required
def change_name():
    back_url = request.args.get('back')
    form_info = {
        "title": "修改用户名",
        "form_action": "/api/change_name",
        "back_url": back_url
    }
    return render_template('form.html', theme=get_user_theme(), user_datas=get_user_datas()[1], form=forms.ChangName(), form_info=form_info)


@main.route("/change_mail")
@login_required
def change_mail():
    back_url = request.args.get('back')
    form_info = {
        "title": "修改邮箱",
        "form_action": "/api/change_mail",
        "back_url": back_url
    }
    return render_template('form.html', theme=get_user_theme(), user_datas=get_user_datas()[1], form=forms.ChangeMail(), form_info=form_info)

@main.route("/change_password")
@login_required
def change_password():
    back_url = request.args.get('back')
    form_info = {
        "title": "修改邮箱",
        "form_action": "/api/change_password",
        "back_url": back_url
    }
    return render_template('form.html', theme=get_user_theme(), user_datas=get_user_datas()[1], form=forms.ChangePassowrd(), form_info=form_info)

@main.route("/user_space/<username>")
@login_required
def userSpace(username):
    user_id = database.get_user_id_by_username(username)
    if user_id["success"]:
        user_datas = get_user_datas(username)
        return render_template('user_space.html', theme=get_user_theme(username), user_datas=get_user_datas()[1] ,target_user_datas=user_datas[1], can_visit=user_datas[0])
    else:
        return render_template("error.html", error_code=404, error_message="The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.", theme=get_user_theme(), user_datas=get_user_datas()[1]), 404

@main.route("/praise_list")
@login_required
def praise_list():
    user_datas = database.get_user(current_user.user_id)["user"]
    praise_list = user_datas["user_space_info"]["praise"]
    praise_uername_list = []
    slogan_list = {}
    for i in praise_list:
        this_user_datas = database.get_user(i)["user"]
        this_username = this_user_datas["user_datas"]["username"]
        this_slogan = this_user_datas["user_space_info"]["slogan"]
        praise_uername_list.append(this_username)
        slogan_list[this_username] = this_slogan
        
    return render_template('praise_list.html', theme=get_user_theme(), user_datas=get_user_datas()[1], praise_list=praise_uername_list, slogan_list=slogan_list)


@main.route("/friend_request")
@login_required
def friend_request():
    user_datas = database.get_user(current_user.user_id)["user"]
    friend_request_list = user_datas["friend_request"]
    friend_request_uername_list = {}
    for i in friend_request_list:
        this_user_datas = database.get_user(int(i))["user"]
        this_username = this_user_datas["user_datas"]["username"]
        friend_request_uername_list[this_username] = friend_request_list[i]
        
    return render_template('friend_request.html', theme=get_user_theme(), user_datas=get_user_datas()[1], friend_request_list=friend_request_uername_list, )


@main.route("/test")
def test():
    from utils import web
    web.send_notification_to_user(1, {"title": "test", "content": "test"})
    return "ok"