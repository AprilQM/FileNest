highlight_menu_item(6)

function get_chat_histroy(target_user_name) {
    $id("chat_box").style.display = "block"
    $id("search_box").style.display = "none"
    $id("title").innerHTML = target_user_name
    $id("view_box").classList.add("right")
    $id("view_box").classList.remove("left")
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