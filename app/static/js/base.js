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
    if ($id("alert_primary").classList.contains("alert_show")) {
        $id("alert_primary").classList.remove("alert_show");
        $id("alert_primary").classList.add("alert_hide");
    }
    if ($id("alert_secondary").classList.contains("alert_show")) {
        $id("alert_secondary").classList.remove("alert_show");
        $id("alert_secondary").classList.add("alert_hide");
    }
    if ($id("alert_success").classList.contains("alert_show")) {
        $id("alert_success").classList.remove("alert_show");
        $id("alert_success").classList.add("alert_hide");
    }
    if ($id("alert_danger").classList.contains("alert_show")) {
        $id("alert_danger").classList.remove("alert_show");
        $id("alert_danger").classList.add("alert_hide");
    }
    if ($id("alert_warning").classList.contains("alert_show")) {
        $id("alert_warning").classList.remove("alert_show");
        $id("alert_warning").classList.add("alert_hide");
    }
    if ($id("alert_info").classList.contains("alert_show")) {
        $id("alert_info").classList.remove("alert_show");
        $id("alert_info").classList.add("alert_hide");
    }
    if ($id("alert_light").classList.contains("alert_show")) {
        $id("alert_light").classList.remove("alert_show");
        $id("alert_light").classList.add("alert_hide");
    }
    if ($id("alert_dark").classList.contains("alert_show")) {
        $id("alert_dark").classList.remove("alert_show");
        $id("alert_dark").classList.add("alert_hide");
    }
}

const alert_duration = 3000;
let alert_hidden;
function primary_alert(message) {
    hiden_alert()
    clearInterval(alert_hidden)
    $id("alert_primary").classList.remove("alert_hide");
    $id("alert_primary").classList.add("alert_show");
    $id("alert_primary").innerHTML = message;
    alert_hidden = setTimeout(hiden_alert, alert_duration)
}
function secondary_alert(message) {
    hiden_alert()
    clearInterval(alert_hidden)
    $id("alert_secondary").classList.remove("alert_hide");
    $id("alert_secondary").classList.add("alert_show");
    $id("alert_secondary").innerHTML = message;
    alert_hidden = setTimeout(hiden_alert, alert_duration)
}
function success_alert(message) {
    hiden_alert()
    clearInterval(alert_hidden)
    $id("alert_success").classList.remove("alert_hide");
    $id("alert_success").classList.add("alert_show");
    $id("alert_success").innerHTML = message;
    alert_hidden = setTimeout(hiden_alert, alert_duration)
}
function danger_alert(message) {
    hiden_alert()
    clearInterval(alert_hidden)
    $id("alert_danger").classList.remove("alert_hide");
    $id("alert_danger").classList.add("alert_show");
    $id("alert_danger").innerHTML = message;
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
function info_alert(message) {
    hiden_alert()
    clearInterval(alert_hidden)
    $id("alert_info").classList.remove("alert_hide");
    $id("alert_info").classList.add("alert_show");
    $id("alert_info").innerHTML = message;
    alert_hidden = setTimeout(hiden_alert, alert_duration)
}
function light_alert(message) {
    hiden_alert()
    clearInterval(alert_hidden)
    $id("alert_light").classList.remove("alert_hide");
    $id("alert_light").classList.add("alert_show");
    $id("alert_light").innerHTML = message;
    alert_hidden = setTimeout(hiden_alert, alert_duration)
}
function dark_alert(message) {
    hiden_alert()
    clearInterval(alert_hidden)
    $id("alert_dark").classList.remove("alert_hide");
    $id("alert_dark").classList.add("alert_show");
    $id("alert_dark").innerHTML = message;
    alert_hidden = setTimeout(hiden_alert, alert_duration)
}

// endregion


// region 加载UI
function create_ui(key) {
    const ui_both = document.createElement("script");
    ui_both.src = `/api/get_ui_creator/both/${key}.js`;
    document.body.appendChild(ui_both);
    const window_width = window.innerWidth;
    const ui_device = document.createElement("script");
    if (window_width < 768) {
        ui_device.src = `/api/get_ui_creator/mobile/${key}.js`;
    } else {
        ui_device.src = `/api/get_ui_creator/pc/${key}.js`;
    }
    document.body.appendChild(ui_device);
}
// endregion

//region 消息提示框
let message_box_timer;
let message_box_show = false;
const message_duration = 3000;
function show_message(title, content, fuc = () => { }, color = "cornflowerblue") {
    if (message_box_show) {
        return;
    }
    const message_box = $id("message_box");
    const message_title = $id("message_title");
    const message_content = $id("message_content");
    message_title.style.color = color;
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