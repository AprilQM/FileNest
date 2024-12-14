highlight_menu_item(4)

function back_to_friend_list() {
    $id("view_box").classList.add("left")
    $id("view_box").classList.remove("right")
}
function to_notification_list(title) {
    $id("view_box").classList.add("right")
    $id("view_box").classList.remove("left")
    $id("title").innerText = title
}