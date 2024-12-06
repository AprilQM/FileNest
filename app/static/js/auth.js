function to_register_form() {
    $id("view_box").classList.add("register")
    $id("view_box").classList.remove("login")
    $id("login_username_input").value = ""
    $id("login_password_input").value = ""
}
function to_login_form() {
    $id("view_box").classList.add("login")
    $id("view_box").classList.remove("register")
    $id("register_mail_input").value = ""
    $id("register_username_input").value = ""
    $id("register_password_input").value = ""
    $id("register_code_input").value = ""
}
// 登录表单提交
let input_hidden;
document.getElementById("login_form").addEventListener("submit", function (event) {

    event.preventDefault();  // 阻止默认提交行为

    // 获取表单数据
    let formData = new FormData(event.target);

    const param = {
        next_url: formData.get("next_url"),
        username: formData.get("username"),
        password: formData.get("password"),
    };
    clearTimeout(input_hidden);
    
    if (!param['username']) {
        $id("login_username_input").style.borderColor = "var(--background_conflict)";
        input_hidden = setTimeout(() => {
            $id("login_username_input").style.borderColor = "var(--background)";
        }, alert_duration);
        error_alert("用户名不能为空");
    } else if (!param['password']) {
        $id("login_password_input").style.borderColor = "var(--background_conflict)";
        input_hidden = setTimeout(() => {
            $id("login_password_input").style.borderColor = "var(--background)";
        }, alert_duration);
        error_alert("密码不能为空");
    }else {
        // 修改表单数据后发送请求
        ajax('POST', '/api/login', param, function (response) { 
            
            if (response["success"]) {
                success_alert("登录成功");
                jump_to_other_page_with_ui(response["next_url"])
            } else {
                if (response["massage"] === "no_user") {
                    $id("login_username_input").style.borderColor = "var(--background_conflict)";
                    input_hidden = setTimeout(() => {
                        $id("login_username_input").style.borderColor = "var(--background)";
                    }, alert_duration);
                    error_alert("用户名不存在");
                } else {
                    $id("login_password_input").style.borderColor = "var(--background_conflict)";
                    input_hidden = setTimeout(() => {
                        $id("login_password_input").style.borderColor = "var(--background)";
                    }, alert_duration);
                    error_alert("密码错误");
                }
            }
        }, function (error) { 
            error_alert(error);
        })
    }
});
// 注册1表单提交
document.getElementById("register_form_1").addEventListener("submit", function (event) {

    event.preventDefault();  // 阻止默认提交行为

    // 获取表单数据
    let formData = new FormData(event.target);

    const param = {
        email: formData.get("email"),
        username: formData.get("username"),
        password: formData.get("password"),
    };
    

    if (!param['email']) {
        $id("register_mail_input").style.borderColor = "var(--background_conflict)";
        input_hidden = setTimeout(() => {
            $id("register_mail_input").style.borderColor = "var(--background)";
        }, alert_duration);
        error_alert("邮箱不能为空");
    } else if (!param['username']) {
        $id("register_username_input").style.borderColor = "var(--background_conflict)";
        input_hidden = setTimeout(() => {
            $id("register_username_input").style.borderColor = "var(--background)";
        }, alert_duration);
        error_alert("用户名不能为空");
    } else if (param['username'].length < 3 || param['username'].length > 12) { 
        
        $id("register_username_input").style.borderColor = "var(--background_conflict)";
        input_hidden = setTimeout(() => {
            $id("register_username_input").style.borderColor = "var(--background)";
        }, alert_duration);
        error_alert("用户名应为3~12位字符");
    } else if (!check_str_legal(param['username'])) {
        $id("register_username_input").style.borderColor = "var(--background_conflict)";
        input_hidden = setTimeout(() => {
            $id("register_username_input").style.borderColor = "var(--background)";
        }, alert_duration);
        error_alert("用户名包含了非法字符");
    }else if (!param['password']) {
        $id("register_password_input").style.borderColor = "var(--background_conflict)";
        input_hidden = setTimeout(() => {
            $id("register_password_input").style.borderColor = "var(--background)";
        }, alert_duration);
        error_alert("密码不能为空");
    }else if (param['password'].length < 6) {
        $id("register_password_input").style.borderColor = "var(--background_conflict)";
        input_hidden = setTimeout(() => {
            $id("register_password_input").style.borderColor = "var(--background)";
        }, alert_duration);
        error_alert("密码应为6位以上字符");
    }
    else { 
        ajax('POST', '/api/register_1', param, function (response) { 
            if (response["massage"] === "fail") {
                if (response["reason"] === "email_exist") {
                    $id("register_mail_input").style.borderColor = "var(--background_conflict)";
                    input_hidden = setTimeout(() => {
                        $id("register_mail_input").style.borderColor = "var(--background)";
                    }, alert_duration);
                    error_alert("邮箱已被注册");
                } else if (response["reason"] === "username_exist") {
                    $id("register_username_input").style.borderColor = "var(--background_conflict)";
                    input_hidden = setTimeout(() => {
                        $id("register_username_input").style.borderColor = "var(--background)";
                    }, alert_duration);
                    error_alert("用户名已被注册");
                } else if (response["reason"] === "username_length_error") {
                    $id("register_username_input").style.borderColor = "var(--background_conflict)";
                    input_hidden = setTimeout(() => {
                        $id("register_username_input").style.borderColor = "var(--background)";
                    }, alert_duration);
                    error_alert("用户名应为3~12位字符");
                }else if (response["reason"] === "password_length_error") {
                    $id("register_password_input").style.borderColor = "var(--background_conflict)";
                    input_hidden = setTimeout(() => {
                        $id("register_password_input").style.borderColor = "var(--background)";
                    }, alert_duration);
                    error_alert("密码应为6位以上字符");
                } else if (response["reason"] === "username_illegal_character") {
                    $id("register_username_input").style.borderColor = "var(--background_conflict)";
                    input_hidden = setTimeout(() => {
                        $id("register_username_input").style.borderColor = "var(--background)";
                    }, alert_duration);
                    error_alert("用户名包含了非法字符");
                }
            } else { 
                $id("register_box").classList.remove("register_1");
                $id("register_box").classList.add("register_2");
            }
        },
        function (error) {
            error_alert(error);
        })
    }
});

// 注册2表单提交
document.getElementById("register_form_2").addEventListener("submit", function (event) {

    event.preventDefault();  // 阻止默认提交行为

    // 获取表单数据
    let formData = new FormData(event.target);

    const param = {
        code: formData.get("code"),
    };

    if (!param['code']) {
        $id("register_code_input").style.borderColor = "var(--background_conflict)";
        input_hidden = setTimeout(() => {
            $id("register_code_input").style.borderColor = "var(--background)";
        }, alert_duration);
        error_alert("验证码不能为空");
    } else {
        ajax('POST', '/api/register_2', param, function (response) {
            if (response["massage"] === "success") {
                success_alert("注册成功");
                $id("register_box").classList.remove("register_2");
                $id("register_box").classList.add("register_1");
                to_login_form();
            } else {
                if (response["reason"] === "code_error") {
                    $id("register_code_input").style.borderColor = "var(--background_conflict)";
                    input_hidden = setTimeout(() => {
                        $id("register_code_input").style.borderColor = "var(--background)";
                    }, alert_duration);
                    error_alert("验证码错误");
                } else if (response["reason"] === "code_timeout") {
                    $id("register_code_input").style.borderColor = "var(--background_conflict)";
                    input_hidden = setTimeout(() => {
                        $id("register_code_input").style.borderColor = "var(--background)";
                    }, alert_duration);
                    error_alert("验证码已过期");
                } else if (response["reason"] === "email_exist") { 
                    $id("register_box").classList.remove("register_2");
                    $id("register_box").classList.add("register_1");
                    $id("register_mail_input").style.borderColor = "var(--background_conflict)";
                    input_hidden = setTimeout(() => {
                        $id("register_mail_input").style.borderColor = "var(--background)";
                    }, alert_duration);
                    error_alert("邮箱已被注册");
                } else if (response["reason"] === "username_exist") { 
                    $id("register_box").classList.remove("register_2");
                    $id("register_box").classList.add("register_1");
                    $id("register_username_input").style.borderColor = "var(--background_conflict)";
                    input_hidden = setTimeout(() => {
                        $id("register_username_input").style.borderColor = "var(--background)";
                    }, alert_duration);
                    error_alert("用户名已被注册");
                }
            }
        }, function (error) {
            error_alert(error);
        })
    }
});

