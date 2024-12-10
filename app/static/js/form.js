document.getElementById("main_form").addEventListener("submit", function (event) {

    event.preventDefault();  // 阻止默认提交行为
    
    submit_datas()
})

function submit_datas() {
    const inputs = document.getElementsByClassName("input");
    let values = []
    for (let i = 0; i < inputs.length; i++) {
        values.push(inputs[i].value)
    }
    const param = {
        "values": values
    }
    ajax("POST", form_info["form_action"], param, function (datas) {
        
        if(datas["success"]){
            success_alert(datas["message"])
            jump_to_other_page_with_ui(form_info["back_url"])
        }else{
            error_alert(datas["message"])
        }

    }, function (err) {
        error_alert(err)
    })
}