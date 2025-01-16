highlight_menu_item(6)

let current_username;
let current_history_page;
function get_chat_histroy(target_user_name) {
    if (current_username) {
        $id(`${current_username}_friend_item`).style.backgroundColor = "var(--background2)"
    }
    
    current_username = target_user_name
    $id(`${current_username}_friend_item`).style.backgroundColor = "var(--secondary2)"
    $id("chat_box").style.display = "block"
    $id("search_box").style.display = "none"
    $id("title").innerHTML = target_user_name
    $id("view_box").classList.add("right")
    $id("view_box").classList.remove("left")
    $id("chat_box").setAttribute("target_user_name", target_user_name)
    $id(target_user_name + "_friend_item").classList.remove("friend_message_box")

    const param = {
        "target_user_name": target_user_name
    }

    ajax('POST', "/api/get_chat_histroy", param, function (response) {
        if (response["success"]) { 
            current_history_page = response["current_history_page"]
            
            // 删除所有聊天记录
            while ($id("chat_content_box").firstChild) {
                $id("chat_content_box").removeChild($id("chat_content_box").firstChild)
            }

            // 显示聊天记录
            for (let i in response["chat_histroy"]) {
                
                const msg_box = document.createElement("div")
                msg_box.classList.add("msg_box")
                const img = document.createElement("img")
                const p = document.createElement("p")
                if (response["chat_histroy"][i][0] === "0") {
                    img.src = "/api/get_user_avatar_small/" + user_data["user_datas"]["username"]
                    img.classList.add("my_avatar")
                    p.classList.add("my_msg")
                    img.onclick = () => {
                        jump_to_other_page_with_ui("/user_space/" + user_data["user_datas"]["username"])
                    }
                } else if (response["chat_histroy"][i][0] === "1") {
                    img.src = "/api/get_user_avatar_small/" + current_username
                    img.classList.add("target_avatar")
                    img.onclick = () => {
                        jump_to_other_page_with_ui("/user_space/" + current_username)
                    }
                    p.classList.add("target_msg")
                }
                p.innerText = response["chat_histroy"][i][1]
                msg_box.appendChild(img)
                msg_box.appendChild(p)
                $id("chat_content_box").appendChild(msg_box)
            }
            $id("chat_content_box").scrollTop = $id("chat_content_box").scrollHeight
        } else {
            error_alert(response["message"])
        }
        
    }, function (error) {
        error_alert(error)
    })
}
function back_to_friend_list() {
    $id("view_box").classList.add("left")
    $id("view_box").classList.remove("right")
    if (current_username) {
        $id(`${current_username}_friend_item`).style.backgroundColor = "var(--background2)"
    }
    current_username = ""
}

function to_search() {
    if($id("search_friend_input").value === ""){
        error_alert("请先输入要搜索的用户名")
        return
    }
    $id("view_box").classList.add("right")
    $id("view_box").classList.remove("left")
    $id("search_box").style.display = "block"
    $id("chat_box").style.display = "none"
    $id("title").innerHTML = "搜索"

    let flag = true

    while($id("my_friends_search_box").firstChild){
        $id("my_friends_search_box").removeChild($id("my_friends_search_box").firstChild)
    }
    for (let i in user_data["friends"]) {
        
        if (i.includes($id("search_friend_input").value)) {
            const div = document.createElement("div")
            div.classList.add("search_item_box")
            const img = document.createElement("img")
            img.src = "/api/get_user_avatar_small/" + i
            const h6 = document.createElement("h6")
            h6.innerHTML = i
            div.appendChild(img)
            div.appendChild(h6)
            div.onclick = function () {
                get_chat_histroy(i)
            }
            $id("my_friends_search_box").appendChild(div)
            flag = false
        }
    }
    if (flag) {
        const h2 = document.createElement("h2")
        h2.id = "my_friends_search_light"
        h2.innerHTML = "你没有拥有该关键词的好友"
        $id("my_friends_search_box").appendChild(h2)
    }

    const param = {
        "username" : $id("search_friend_input").value
    }

    ajax('POST', "/api/search_user", param, function (response) {
        while($id("all_user_search_box").firstChild){
                $id("all_user_search_box").removeChild($id("all_user_search_box").firstChild)
            }
        if (response["success"]) {
            const div = document.createElement("div")
            div.classList.add("search_item_box")
            const img = document.createElement("img")
            img.src = "/api/get_user_avatar_small/" + param["username"]
            const h6 = document.createElement("h6")
            h6.innerHTML = $id("search_friend_input").value
            div.appendChild(img)
            div.appendChild(h6)
            div.onclick = function () {
                jump_to_other_page_with_ui("/user_space/" + param["username"])
            }
            $id("all_user_search_box").appendChild(div)
        } else {
            const h2 = document.createElement("h2")
            h2.id = "my_friends_search_light"
            h2.innerHTML = "该用户不存在"
            $id("all_user_search_box").appendChild(h2)
        }
    }, function (error) {
        error_alert(error)
    })
}

let function_box_state = false
function show_function_box(){
    if(!function_box_state){
        $id("friend_function_box").classList.add("friend_function_box_show")
        $id("friend_function_box").classList.remove("friend_function_box_hide")
        function_box_state = true
    }
}
function hide_function() {
    if(function_box_state){
        $id("friend_function_box").classList.remove("friend_function_box_show")
        $id("friend_function_box").classList.add("friend_function_box_hide")
        function_box_state = false
    }
}

function  show_confirm_delete() {
    show_input_box("输入好友名字，以确认解除关系", "delete_friend()", "var(--background_conflict)", "24px")
}
function delete_friend() {

    if ($id("gray_input").value === $id("chat_box").getAttribute("target_user_name")) {
        const param = {
            "username": $id("chat_box").getAttribute("target_user_name")
        }
        ajax('POST', "/api/delete_friend", param, function (response) {
            if (response["success"]) {
                current_username = null
                back_to_friend_list()
                hide_function()
                success_alert("删除好友成功")

                while ($id("friends_item_list_box").firstChild) {
                    $id("friends_item_list_box").removeChild($id("friends_item_list_box").firstChild)
                }
                
                for (let i in response["friend_list"]) {
                    
                    const div = document.createElement("div")
                    div.classList.add("friend_item_box")
                    div.id = i + "_friend_item"
                    if (response["friend_list"][i][0]) {
                        div.classList.add("friend_message_box")
                    }
                    const img = document.createElement("img")
                    img.src = "/api/get_user_avatar_small/" + i
                    img.classList.add("friends_list_avatar")
                    const div2 = document.createElement("div")
                    div2.classList.add("friend_info")
                    const p1 = document.createElement("p")
                    p1.classList.add("friends_list_username")
                    p1.innerHTML = i
                    const p2 = document.createElement("p")
                    p2.classList.add("friends_list_slogan")
                    p2.innerHTML = user_data["friends"][i][1]
                    div2.appendChild(p1)
                    div2.appendChild(p2)
                    div.appendChild(img)
                    div.appendChild(div2)
                    div.onclick = function () {
                        get_chat_histroy(i)
                    }
                    $id("friends_item_list_box").appendChild(div)
                }

            } else {
                error_alert("删除好友失败")
            }
        }, function (error) {
            error_alert(error)
        })
    } else {
        error_alert("输入的用户名不正确")
    }
}
$id("chat_input").addEventListener("keydown", function (event) {
    if (event.keyCode === 13) {
        if (event.ctrlKey || event.shiftKey) {
            // 换行
            event.preventDefault()
            $id("chat_input").value += "\n"
        } else {
            send_message()
            event.preventDefault()
        }
    }
})
function send_message() {
    const message = $id("chat_input").value
    
    if (!message.trim()) {
        error_alert("消息不能为空！")
        return
    }
    const param = {
        "target_user_name": $id("chat_box").getAttribute("target_user_name"),
        "message": message
    }
    ajax('POST', "/api/send_message", param, function (response) {
        if (response["success"]) {
            $id("chat_input").value = ""
            const msg_box = document.createElement("div")
            msg_box.classList.add("msg_box")
            const img = document.createElement("img")
            img.src = "/api/get_user_avatar_small/" + user_data["user_datas"]["username"]
            img.classList.add("my_avatar")
            img.onclick = () => {
                jump_to_other_page_with_ui("/user_space/" + user_data["user_datas"]["username"])
            }
            const p = document.createElement("p")
            p.classList.add("my_msg")
            p.innerText = message
            msg_box.appendChild(img)
            msg_box.appendChild(p)
            $id("chat_content_box").appendChild(msg_box)
            $id("chat_content_box").scrollTop = $id("chat_content_box").scrollHeight

        } else {
            error_alert("发送失败")
        }
    }, function (error) {
        error_alert(error)
    })
}

const chat_socket = io('/chat');

chat_socket.on('connect', function() {
    console.log("聊天已连接");
});

chat_socket.on('message', function (data) {
    if (data._from === current_username) {
        const msg_box = document.createElement("div")
        msg_box.classList.add("msg_box")
        const img = document.createElement("img")
        img.src = "/api/get_user_avatar_small/" + data._from
        img.classList.add("target_avatar")
        img.onclick = () => {
            jump_to_other_page_with_ui("/user_space/" + current_username)
        }
        const p = document.createElement("p")
        p.classList.add("target_msg")
        p.innerText = data.content
        msg_box.appendChild(img)
        msg_box.appendChild(p)
        $id("chat_content_box").appendChild(msg_box)
        $id("chat_content_box").scrollTop = $id("chat_content_box").scrollHeight
    } else {
        $id(data._from + "_friend_item").classList.add("friend_message_box")
        
        // 告知后端要写入文件
        chat_socket.emit("set_unread", {"username": data._from})
    }
});

chat_socket.on('disconnect', function() {
    console.log("聊天已断开");
});

// 监听滚轮事件
let old_scroll_height = 0;
$id("chat_content_box").addEventListener("wheel", (event) => { 
    if ($id("chat_content_box").scrollTop === 0 && event.deltaY < 0) {
        const param = {
            "target_user_name": $id("chat_box").getAttribute("target_user_name"),
            "current_history_page": current_history_page
        }
        old_scroll_height = $id("chat_content_box").scrollHeight
        ajax('POST', "/api/get_last_message_page", param, function (response) {
            if (response["success"]) {
                current_history_page = response["current_history_page"]
                for (let i in response["last_page_content"]) {
                    
                    const msg_box = document.createElement("div")
                    msg_box.classList.add("msg_box")
                    const img = document.createElement("img")
                    const p = document.createElement("p")
                    if (response["last_page_content"][i][0] === "0") {
                        img.src = "/api/get_user_avatar_small/" + user_data["user_datas"]["username"]
                        img.classList.add("my_avatar")
                        p.classList.add("my_msg")
                        img.onclick = () => {
                            jump_to_other_page_with_ui("/user_space/" + user_data["user_datas"]["username"])
                        }
                    } else if (response["last_page_content"][i][0] === "1") {
                        img.src = "/api/get_user_avatar_small/" + current_username
                        img.classList.add("target_avatar")
                        img.onclick = () => {
                            jump_to_other_page_with_ui("/user_space/" + current_username)
                        }
                        p.classList.add("target_msg")
                    }
                    p.innerText = response["last_page_content"][i][1]
                    msg_box.appendChild(img)
                    msg_box.appendChild(p)
                    $id("chat_content_box").prepend(msg_box)
                }

                $id("chat_content_box").scrollTop = $id("chat_content_box").scrollHeight - old_scroll_height - 30 //-30是为了让这次滑动有互动

            } else {
                warning_alert("上面已经没有消息啦！")
            }
        })
    }
})