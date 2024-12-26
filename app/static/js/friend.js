highlight_menu_item(6)

let current_username;
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


    ajax('POST', "/api/get_chat_histroy",param, function (response) {
        
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
    show_input_box("输入好友名字，以接触关系", "delete_friend()", "var(--background_conflict)", "24px")
}
function delete_friend() {
    console.log($id("gray_input").value, $id("chat_box").getAttribute("target_user_name"));

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
