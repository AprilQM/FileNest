highlight_menu_item(6)

function get_chat_histroy(element, target_user_name) {
    element.classList.remove("friend_message_box")
    
    const param = {
        "target_user_name": target_user_name
    }

    ajax('POST', "/api/get_chat_histroy",param, function (response) {
        
    }, function (error) {
        error_alert(error)
    })
}