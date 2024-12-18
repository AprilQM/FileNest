highlight_menu_item(4)

function back_to_friend_list() {
    $id("view_box").classList.add("left")
    $id("view_box").classList.remove("right")
}

function to_notification_list(title) {
    $id("view_box").classList.add("right")
    $id("view_box").classList.remove("left")
    $id("title").innerText = title

    while ($id("notification_content_box").firstChild) {
        $id("notification_content_box").removeChild($id("notification_content_box").firstChild)
    }

    const notification_dict = {
            "登录": "login",
            "好友": "friend",
            "系统": "server",
            "其他": "other"
        }
    const param = {
        "type": notification_dict[title]
    }
    ajax('POST', "/api/get_notification", param, function (response) {

        // 取最新的15条消息
        const will_show_notification = response["notification"].slice(-15)

        for (let i of will_show_notification) {
            const notification_item_box = document.createElement("div")
            notification_item_box.classList.add("notification_item_box")
            const notification_item_title = document.createElement("h1")
            notification_item_title.classList.add("notification_item_title")
            const notification_item_content = document.createElement("p")
            notification_item_content.classList.add("notification_item_content")
            const notification_item_time = document.createElement("span")
            notification_item_time.classList.add("notification_item_time")
    
            
            let content;
            if (title === "登录") {
                notification_item_title.innerText = "有设备登录了账号"
                content = `设备系统: ${i["os"]}
                                设备浏览器: ${i["browser"]}
                                设备IP: ${i["ip"]}`
                notification_item_content.innerText = content
            } else if (title === "其他"){
                notification_item_title.innerText = i["title"]
                content = `有新的用户为你的个人主页点赞了，这个用户是：<a href="/user_space/${i["username"]}" class="notification_item_a">${i["username"]}</a>，快去他的主页回赞他吧~`
                notification_item_content.innerHTML = content
            }
            
            notification_item_time.innerText = i["time"]
    
            notification_item_box.appendChild(notification_item_title)
            notification_item_box.appendChild(notification_item_content)
            notification_item_box.appendChild(notification_item_time)
    
            $id("notification_content_box").appendChild(notification_item_box)
        }

        // 将滚轮滚到最底部
        $id("notification_content_box").scrollTop = $id("notification_content_box").scrollHeight
        
        
        
    }, function (error) {
        error_alert(error)
    })
    
}

// 默认显示登录消息
to_notification_list("登录")