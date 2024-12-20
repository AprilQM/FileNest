highlight_menu_item(5)

let color_box_state = false
function open_change_ui_color_box() {
    if(color_box_state) {
        color_box_state = false
        $id("color_box").style.height = "80px"
    } else {
        color_box_state = true
        $id("color_box").style.height = "150px"
    }
}

function change_to_this_color(color) {
    ajax('POST', '/api/change_ui_color', { "color": color }, function(data) {
        if (data["success"]) {
            const root = document.documentElement;
            root.style.setProperty('--main', data["colors"]["colors"]["main"]);
            root.style.setProperty('--secondary1', data["colors"]["colors"]["secondary1"]);
            root.style.setProperty('--secondary2', data["colors"]["colors"]["secondary2"]);
            root.style.setProperty('--prominent', data["colors"]["colors"]["prominent"]);
            root.style.setProperty('--background', data["colors"]["colors"]["background"]);
            root.style.setProperty('--background2', data["colors"]["colors"]["background2"]);
            root.style.setProperty('--background_conflict', data["colors"]["colors"]["background_conflict"]);
            root.style.setProperty('--text', data["colors"]["colors"]["text"]);
            root.style.setProperty('--text2', data["colors"]["colors"]["text2"]);
            root.style.setProperty('--text3', data["colors"]["colors"]["text3"]);
            root.style.setProperty('--other', data["colors"]["colors"]["other"]);

            $id("theme_name_text").innerText = data["colors"]["name"]
            
            color_box_state = false
            $id("color_box").style.height = "80px"

        } else {
            error_alert("无权修改为次颜色")
        }
        
    }, function (error) {
        error_alert(error)
    })
}

function change_privacy_mode(){
    ajax('POST', '/api/change_privacy_mode', null, function(data){
        if (data["success"]) {
            $id("privacy_text").innerText = ["公开", "好友", "隐藏"][data["state"]]
        }
    }, 
    function(err){
        error_alert(err)
    })
}