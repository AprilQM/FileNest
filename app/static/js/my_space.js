function check_in() {
    ajax("POST", "/api/check_in", null, function (data) {
        
        if (data["success"]) {
            const root = document.documentElement;
            $id("have_checked_light").style.display = "block"
            $id("check_in_btn").style.display = "none"
            root.style.setProperty('--check_in_days', data["check_in_days"]);
            root.style.setProperty('--next_level_need_days', data["next_level_need_days"]); 
            $id("level_text").innerText = `${data["check_in_days"]}/${data["next_level_need_days"]}`

            user_data["other"]["can_check"] = false;
            
            user_data["user_datas"]["check_in_days"] = data["check_in_days"]
            user_data["user_datas"]["next_level_need_days"] = data["next_level_need_days"]

            $id("level_icon").classList.remove("icon-level-" + user_data["user_datas"]["level"])
            user_data["user_datas"]["level"] = data["level"]
            $id("level_icon").classList.add("icon-level-" + user_data["user_datas"]["level"])
        }
    }, function () {
        error_alert("签到失败，网络错误")
        $id("have_checked_light").style.display = "none"
        $id("check_in_btn").style.display = "block"
    })
}
if (user_data["other"]["can_check"]) {
    $id("have_checked_light").style.display = "none"
    $id("check_in_btn").style.display = "block"
} else {
    $id("have_checked_light").style.display = "block"
    $id("check_in_btn").style.display = "none"
}