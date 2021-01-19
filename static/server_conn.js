var server = "http://35.193.159.169:5000";
var send_msg = {'name':"",'days': "",'requestID':""};
//var send_msg2 = {'days':""};


function update_var()
{
    var name = String($("#name").val());
    var days = String($("#days").val());

    send_msg['name','days']={name,days};
    var randInt = String(Math.floor(Math.random() * (999999 - 1000 + 1)) + 1000);
    randInt = String(randInt);
    send_msg['requestID'] = {randInt}
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
    console.log(server)

    $.ajax({
            type: "POST",
            url:server + appdir,
            data: JSON.stringify(send_msg),
            dataType: 'json',
            contentType: 'application/json',
        }).done(function(data) {
            var graph = data['graph'];
            const byteCharacters = atob(graph);
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {
                byteNumbers[i] = byteCharacters.charCodeAt(i);
            }
            const byteArray = new Uint8Array(byteNumbers);
//            var graph = btoa(data['graph']);
            var blob = new Blob( [ byteArray ], { type: "image/png" } );
            var urlCreator = window.URL || window.webkitURL;
            var imageUrl = urlCreator.createObjectURL( blob );
            $('#imgContainer').append('<img src="' + imageUrl + '" />');
            $('#Response').html(data['message'].bold());
        });

}