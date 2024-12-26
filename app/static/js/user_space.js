if (target_user_datas["user_datas"]["user_id"] !== 0) {
    for (let i of target_user_datas["user_space_info"]["tag"]) {
        const b = document.createElement("b")
        b.className = "tag"
        b.innerText = i[0]
        b.style.backgroundColor = i[1]
        $id("tag_box").appendChild(b)
    }
    $id("praise_btn_box").addEventListener("click", (e) => {
        if (target_user_datas["is_praise"]) {
            warning_alert("你已经点过赞喽~")
        } else {
            
            ajax("POST", "/api/praise_user", {
                "target_id": target_user_datas["user_datas"]["user_id"],
            }, function (datas) {
                
                if (datas["success"]) {
                    success_alert("点赞成功")
                    target_user_datas["is_praise"] = true
    
                    // 更新点赞数
                    $id("praise_count").innerText = datas["praise_count"]
                    $id("praise_btn").style.color = "var(--background_conflict)"
                    $id("praise_count").style.color = "var(--background_conflict)"
    
    
                } else {
                    error_alert("已经点过啦~")
                }
            }, function (err) {
                error_alert(err)
            })
        }
    })
}

function friend_add(username){
    show_input_box("给Ta的留言", `friend_request_submit("${username}", $id("gray_input").value)`)
}
function friend_request_submit(username, text){
    const param = {
        "username" : username,
        "text" : text
    }
    ajax('POST', "/api/add_friend", param, function(response){
        if (response["success"]){
            success_alert("成功提交申请")
        }else{
            if (response["msg"] === "request_already"){
                error_alert("你已经提交过申请了")
            }else if(response["msg"] === "friend_already"){
                error_alert("你已经是对方的好友了")
            }else if(response["msg"] === "no_user"){
                error_alert("对方不存在")
            }else if(response["msg"] === "can_add_self"){
                error_alert("不能添加自己为好友")
            }
        }
    }, 
    function(err){
        error_alert(err)
    })
}