function jump_to_other_page_with_ui(url) {
    if (url !== window.location.pathname) {  
        loading.in()
        setTimeout(() => {
            window.location.href = url
        }, 690)
    } else {
        error_alert("不是已经在这个页面了嘛？ (；￣Д￣)？  ")
    }
}

// 监听所有a标签的点击时间，并在点击之后触发jump_to_other_page_with_ui函数
document.addEventListener('click', function (event) {
    const target = event.target.closest('a');
    if (target && target.tagName === 'A') {
        event.preventDefault();

        // 获取跳转的 URL
        const href = target.href;
        jump_to_other_page_with_ui(href)
    }
});

function ajax(method, url, data, successCallback, errorCallback) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');

    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status >= 200 && xhr.status < 300) {
                if (successCallback) {
                    successCallback(JSON.parse(xhr.responseText), xhr.status);
                }
            } else {
                if (errorCallback) {
                    errorCallback(xhr.statusText, xhr.status);
                }
            }
        }
    };

    xhr.onerror = function () {
        if (errorCallback) {
            errorCallback('Network Error', xhr.status);
        }
    };

    if (data) {
        xhr.send(JSON.stringify(data));
    } else {
        xhr.send();
    }
}
function copy(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function () {
        }).catch(function (err) {
            console.error('Could not copy text: ', err);
        });
    } else {
        // Fallback for browsers that do not support navigator.clipboard
        const textArea = document.createElement("textarea");
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
        } catch (err) {
            console.error('Could not copy text: ', err);
        }
        document.body.removeChild(textArea);
    }
}
function $id(key) {
    return document.getElementById(key)
}


// region 警告框显示集

function hiden_alert() {
    if ($id("alert_success").classList.contains("alert_show")) {
        $id("alert_success").classList.remove("alert_show");
        $id("alert_success").classList.add("alert_hide");
    }
    if ($id("alert_error").classList.contains("alert_show")) {
        $id("alert_error").classList.remove("alert_show");
        $id("alert_error").classList.add("alert_hide");
    }
    if ($id("alert_warning").classList.contains("alert_show")) {
        $id("alert_warning").classList.remove("alert_show");
        $id("alert_warning").classList.add("alert_hide");
    }
}

const alert_duration = 3000;
let alert_hidden;
function success_alert(message) {
    hiden_alert()
    clearInterval(alert_hidden)
    $id("alert_success").classList.remove("alert_hide");
    $id("alert_success").classList.add("alert_show");
    $id("alert_success").innerHTML = message;
    alert_hidden = setTimeout(hiden_alert, alert_duration)
}
function error_alert(message) {
    hiden_alert()
    clearInterval(alert_hidden)
    $id("alert_error").classList.remove("alert_hide");
    $id("alert_error").classList.add("alert_show");
    $id("alert_error").innerHTML = message;
    alert_hidden = setTimeout(hiden_alert, alert_duration)
}
function warning_alert(message) {
    hiden_alert()
    clearInterval(alert_hidden)
    $id("alert_warning").classList.remove("alert_hide");
    $id("alert_warning").classList.add("alert_show");
    $id("alert_warning").innerHTML = message;
    alert_hidden = setTimeout(hiden_alert, alert_duration)
}

// endregion


//region 消息提示框
const message_duration = 5000;
let message_box_show = false;
let message_box_timer = null;
let alertClickHandler = null; // 用来保存事件监听器引用

function show_message(title, content, fuc = () => { }) {
    if (message_box_show) {
        return;
    }
    const message_box = $id("message_box");
    const message_title = $id("message_title");
    const message_content = $id("message_content");
    message_title.innerHTML = title;
    message_content.innerHTML = content;
    
    // 清除之前的计时器
    clearInterval(message_box_timer);
    
    // 显示消息框
    message_box.classList.remove("message_hide");
    message_box.classList.add("message_show");

    // 如果之前绑定过点击事件，移除之前的事件监听器
    if (alertClickHandler) {
        message_box.removeEventListener("click", alertClickHandler);
    }

    // 新的事件监听器
    alertClickHandler = () => {
        if (message_box_show) {
            clearInterval(message_box_timer);
            message_box.classList.remove("message_show");
            message_box.classList.add("message_hide");
            message_box_show = false;
            fuc(); // 执行回调函数
        }
    };

    // 绑定新的点击事件
    message_box.addEventListener("click", alertClickHandler);

    // 设置定时器关闭消息框
    message_box_timer = setTimeout(() => {
        message_box.classList.remove("message_show");
        message_box_show = false;
    }, message_duration);
    message_box_show = true;
}

const broadcast_socket = io("/broadcast");

broadcast_socket.on('connect', function() {
    console.log("广播已连接");
});

broadcast_socket.on('message', function(msg) {
    show_message(msg.title, msg.content, () => {
        const t = new Function(msg.fuc)
        t();
    })
});

broadcast_socket.on('disconnect', function() {
    console.log("广播已断开");
});

broadcast_socket.on('fuc', function(fuc) {
    const t = new Function(fuc)
    t();
});



//endregion

//region 左侧菜单
const menu_box_pc = $id("menu_box_pc");
const menu_show_btn_pc = $id("menu_show_btn_pc");
const menu_view_box_pc = $id("menu_view_box_pc");
const menu_item_hide_pc = document.getElementsByClassName("menu_item_hide_pc");
const menu_item_show_pc = document.getElementsByClassName("menu_item_show_pc");
let menu_state_pc = false;
menu_show_btn_pc.addEventListener("click", (event) => {
    if (menu_state_pc) {
        menu_state_pc = false;
        menu_view_box_pc.classList.add("menu_close_state")
        menu_view_box_pc.classList.remove("menu_open_state")
        menu_box_pc.style.width = "100px";
        menu_show_btn_pc.style.transform = "scale(1)";
        Array.from(menu_item_show_pc).forEach(item => {
            item.classList.add("menu_item_hide_pc");
            item.classList.remove("menu_item_show_pc");
        });
        
    } else {
        menu_state_pc = true;
        menu_view_box_pc.classList.add("menu_open_state")
        menu_view_box_pc.classList.remove("menu_close_state")
        menu_box_pc.style.width = "300px";
        menu_show_btn_pc.style.transform = "scale(1.05)";
        Array.from(menu_item_hide_pc).forEach(item => {
            item.classList.add("menu_item_show_pc");
            item.classList.remove("menu_item_hide_pc");
        });
    }
});
// 当前页面的菜单项高亮
function highlight_menu_item(index) { 
    const menu_list_pc = [
        $id("to_home_button_pc"),
        $id("to_cloud_button_pc"),
        $id("to_project_button_pc"),
        $id("to_forum_button_pc"),
        $id("to_mail_button_pc"),
        $id("to_setting_button_pc"),
        $id("to_friend_button_pc"),
        
    ]
    const menu_list_mobile = [
        $id("to_home_button_mobile"),
        $id("to_cloud_button_mobile"),
        $id("to_project_button_mobile"),
        $id("to_forum_button_mobile"),
        $id("to_mail_button_mobile"),
        $id("to_setting_button_mobile"),
        $id("to_friend_button_mobile"),
        $id("to_user_space_button_mobile"),
    ]
    if (index !== 7){
        menu_list_pc[index].classList.add("menu_this_page_pc");
    }
    menu_list_mobile[index].classList.add("menu_this_page_mobile");
}
//endregion

// region 其他功能
const illegal_characters = [
        '/', '\\', ':', '*', '?', '"', "'", '<', '>', '|', ';',
        '?', '&', '#', '%', '=', '+',
        '<', '>', '"', "'", '/',
        '(', ')', '[', ']', '{', '}', '^', '$', '.', '*', '+', '?', '|',
        '~', '$',
        '\r', '\n', '\t',
        ' ', ',', '@'
]
    
function check_str_legal(str) {
    for (let i = 0; i < illegal_characters.length; i++) {
        if (str.includes(illegal_characters[i])) {
            return false;
        }
    }
    return true;
}
const notification_socket = io("/notification")

notification_socket.on('connect', function() {
    console.log("通知已连接");
});

notification_socket.on('message', function (msg) {

    show_message(msg.data.title, msg.data.content, () => {
        if (msg.data.fuc) {
            const t = new Function(msg.data.fuc)
            t();
        }
    })
    
});

notification_socket.on('chat_notification', function (msg) {
    // 判断当前的url
    const current_url = window.location.pathname;
    
    if (current_url !== "/friend") { 
        console.log(msg);
        
        show_message(msg.sender_username, `你有一条来自${msg.sender_username}的新消息，点击跳转到好友界面`, () => {
            jump_to_other_page_with_ui("/friend")
        })
    }
});

notification_socket.on('disconnect', function() {
    console.log("通知已断开");
});
// endregion

// region 全屏灰屏
function hide_gray(){
    $id("gray_backgrouand").classList.add("gray_hide")
    $id("gray_backgrouand").classList.remove("gray_show")
    $id("gray_input").value = ""
}
function show_input_box(title, fuc=undefined, color="var(--background_conflict)", size="35px"){
    $id("gray_backgrouand").classList.add("gray_show")
    $id("gray_backgrouand").classList.remove("gray_hide")
    $id("gray_input_box").style.display = "flex"
    $id("gray_input_title").innerText = title
    $id("gray_input_title").style.color = color
    $id("gray_input_title").style.fontSize = size

    $id("gray_input").onkeydown = function(event){
        if(event.key === 'Enter'){
            run_gray_input_fuc(fuc)
        }
    }

    $id("gray_input_yes").onclick = function(){
        run_gray_input_fuc(fuc)
    }
}

function run_gray_input_fuc(fuc){
    const t = new Function(fuc)
    t()
    hide_gray()
}


//endregion