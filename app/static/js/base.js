const loading = {
    container: document.getElementById('loading'),
    out() {
        this.container.classList.remove('loading-in')
        this.container.classList.add('loading-out')
    },
    in() {
        this.container.classList.remove('loading-out')
        this.container.classList.add('loading-in')
    }
}

// 使用 pageshow 事件，确保每次进入页面（包括通过返回键进入）都触发加载效果
window.addEventListener('pageshow', (event) => {
    loading.out();
});

function jump_to_other_page_with_ui(url) {
    loading.in()
    setTimeout(() => {
        window.location.href = url
    }, 1200)
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
            console.log('Copied to clipboard successfully!');
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
            console.log('Copied to clipboard successfully!');
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
let message_box_timer;
let message_box_show = false;
const message_duration = 3000;
function show_message(title, content, fuc = () => { }) {
    if (message_box_show) {
        return;
    }
    const message_box = $id("message_box");
    const message_title = $id("message_title");
    const message_content = $id("message_content");
    message_title.innerHTML = title;
    message_content.innerHTML = content;
    clearInterval(message_box_timer);
    message_box.classList.remove("message_hide");
    message_box.classList.add("message_show");
    message_box_timer = setTimeout(() => {
        message_box.classList.remove("message_show");
        message_box_show = false;
    }, message_duration);
    message_box_show = true;

    // 设置点击事件
    message_box.addEventListener("click", () => {
        if (message_box_show) {
            clearInterval(message_box_timer);
            message_box.classList.remove("message_show");
            message_box.classList.add("message_hide");
            message_box_show = false;
            fuc()
        }
    });
}
//endregion

//region 左侧菜单
const menu_box_pc = $id("menu_box_pc");
const menu_show_btn_pc = $id("menu_show_btn_pc");
let menu_state_pc = false;
menu_show_btn_pc.addEventListener("click", (event) => {
    if (menu_state_pc) {
        menu_box_pc.style.width = "100px";
        menu_state_pc = false;
    } else {
        menu_box_pc.style.width = "300px";
        menu_state_pc = true;
    }
});