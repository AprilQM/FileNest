function to_register_form() {
    $id("view_box").classList.add("register")
    $id("view_box").classList.remove("login")
}
function to_login_form() {
    $id("view_box").classList.add("login")
    $id("view_box").classList.remove("register")
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
            console.log(response);
            
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