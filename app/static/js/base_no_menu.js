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
    if (url !== window.location.pathname) {  
        loading.in()
        setTimeout(() => {
            window.location.href = url
        }, 1200)
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

var socket = io("/broadcast");

socket.on('connect', function() {
    console.log("广播已连接");
});

socket.on('message', function(msg) {
    show_message(msg.title, msg.content, () => {
        const t = new Function(msg.fuc)
        t();
    })
});

socket.on('disconnect', function() {
    console.log("广播已断开");
});
//endregion