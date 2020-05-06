var server = "http://127.0.0.1:5000";
var send_msg = {'name':"",'days': ""};
//var send_msg2 = {'days':""};


function update_var()
{
    var name = String($("#name").val());
    var days = String($("#days").val());

    send_msg['name','days']={name,days};
    //send_msg['days']= days;
    // send_msg2['days']=days;
    // console.log(send_msg);
    // console.log("updatte");
    
    console.log("update var")
}

function send_button()
{
    var appdir="/";
    update_var();
    console.log(send_msg)

    $.ajax({
            type: "POST",
            url:server + appdir,
            data: JSON.stringify(send_msg),
            dataType: 'json',
            contentType: 'application/json',
        }).done(function(data) {
            $('#Response').html(data['message']);
        });

}