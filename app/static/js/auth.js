function to_register_form() {
    $id("view_box").classList.add("register")
    $id("view_box").classList.remove("login")
}
function to_login_form() {
    $id("view_box").classList.add("login")
    $id("view_box").classList.remove("register")
}