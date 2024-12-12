highlight_menu_item(6)

function check_in() {
    ajax("POST", "/api/check_in", null, function (data) {
        
        if (data["success"]) {
            const root = document.documentElement;

            $id("check_in_btn").innerText = "已签到"
            $id("check_in_btn").classList.add("disabled")

            root.style.setProperty('--check_in_days', data["check_in_days"]);
            root.style.setProperty('--next_level_need_days', data["next_level_need_days"]); 
            $id("level_text").innerText = `${data["check_in_days"]}/${data["next_level_need_days"]}`

            user_data["other"]["can_check"] = false;
            
            user_data["user_datas"]["check_in_days"] = data["check_in_days"]
            user_data["user_datas"]["next_level_need_days"] = data["next_level_need_days"]

            $id("user_info_level").classList.remove("icon-level-" + user_data["user_datas"]["level"])
            user_data["user_datas"]["level"] = data["level"]
            $id("user_info_level").classList.add("icon-level-" + user_data["user_datas"]["level"])
        }
    }, function () {
        error_alert("签到失败，网络错误")
        $id("check_in_btn").innerText = "签到"
        $id("check_in_btn").classList.remove("disabled")
    })
}
for(let i of user_data["user_space_info"]["tag"]){
    const b = document.createElement("b")
    b.className = "tag"
    b.innerText = i[0]
    b.style.backgroundColor = i[1]
    $id("tag_box").appendChild(b)
}

$id("slogan_text").value = user_data["user_space_info"]["slogan"]

function change_slogan() {
    if ($id("slogan_text").value.length > 60) {
        warning_alert("标语过长")
        return
    }
    if ($id("slogan_text").value == user_data["user_space_info"]["slogan"]) {
        return
    }
    ajax("POST", "/api/change_slogan", {
        "slogan": $id("slogan_text").value
    }, function (data) {
        if (data["success"]) {
            user_data["user_space_info"]["slogan"] = $id("slogan_text").value
            success_alert("空间标语修改成功！")
        }
    }, function () {
        error_alert("修改失败，网络错误")
    })
}