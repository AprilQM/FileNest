function agree_request(username) {
    const param = {
        "username": username,
        "is_agree": true
    }
    
    ajax('POST', "/api/friend_request", param, function (response) {
        if (response["success"]) {
            success_alert(`${username} 已经是你的好友了`)

            const friend_request_list = response["friend_request_list"]
            create_friend_request_list(friend_request_list)
            
        }
    }, function (err) {
        error_alert(err)
    })
}
function reject_request(username) {
    const param = {
        "username": username,
        "is_agree": false
    }
    ajax('POST', "/api/friend_request", param, function (response) {
        if (response["success"]) {
            success_alert(`成功拒绝 ${username} 的好友请求`)

            const friend_request_list = response["friend_request_list"]
            create_friend_request_list(friend_request_list)
            
        }
    }, function (err) {
        error_alert(err)
    })
}

function create_friend_request_list(friend_request_list) { 
    //清除原来的friend_request_list
    const friend_request_list_box = $id("friend_request_list_box")
    while (friend_request_list_box.firstChild) {
        friend_request_list_box.removeChild(friend_request_list_box.firstChild)
    }

    for (let i in friend_request_list) {
        const friend_request_item_box = document.createElement("div")
        friend_request_item_box.className = "friend_request_item_box box"
        const img = document.createElement("img")
        img.src = `/api/get_user_avatar_small/${i}`
        img.alt = i
        const info_box = document.createElement("div")
        info_box.className = "info_box"
        const h2 = document.createElement("h2")
        h2.innerHTML = i
        const h6 = document.createElement("h6")
        h6.innerHTML = friend_request_list[i]
        const btn_box = document.createElement("div")
        btn_box.className = "btn_box"
        const yes = document.createElement("button")
        yes.className = "yes"
        yes.innerHTML = "同意"
        yes.onclick = function () {
            agree_request(i)
        }
        const no = document.createElement("button")
        no.className = "no"
        no.innerHTML = "拒绝"
        no.onclick = function () {
            reject_request(i)
        }

        info_box.appendChild(h2)
        info_box.appendChild(h6)
        btn_box.appendChild(yes)
        btn_box.appendChild(no)
        friend_request_item_box.appendChild(img)
        friend_request_item_box.appendChild(info_box)
        friend_request_item_box.appendChild(btn_box)
        friend_request_list_box.appendChild(friend_request_item_box)
    }

}