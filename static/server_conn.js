var server = "http://34.69.17.141:5000";
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


}

function isPositiveInteger(n) {
    return n >>> 0 === parseFloat(n);
}

function send_button()
{
    var appdir="/";
    update_var();
    console.log(send_msg)
    console.log(server)

    var name = String($("#name").val());
    var days = String($("#days").val());
    if (name.length == 0) {
        $('#Response').html('Please enter a valid NASDAQ stock ticker.'.bold());
        return false;
    }
    if (days.length == 0 || !isPositiveInteger(days)) {
        $('#Response').html('Please enter an integer for number of days.'.bold());
        return false;
    }
    if (parseInt(days) < 1 || parseInt(days) > 10000) {
        $('#Response').html('Please enter an integer for number of days between 1 and 10000.'.bold());
        return false;
    }


    $.ajax({
            type: "POST",
            url:server + appdir,
            data: JSON.stringify(send_msg),
            dataType: 'json',
            contentType: 'application/json',
        }).done(function(data) {
            if (data['message'].includes('predicted price') ) {
                var graph = data['graph'];
                const byteCharacters = atob(graph);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }
                const byteArray = new Uint8Array(byteNumbers);
                var blob = new Blob( [ byteArray ], { type: "image/png" } );
                var urlCreator = window.URL || window.webkitURL;
                var imageUrl = urlCreator.createObjectURL( blob );
                $('#imgContainer').append('<img src="' + imageUrl + '" />');
            }
            $('#Response').html(data['message'].bold());
        });

}