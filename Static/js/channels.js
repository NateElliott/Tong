function init(data) {

    var data = JSON.parse(data);
    var message = document.getElementById('messageText')
    var messageLog = document.getElementById('channelOutput')

    var chatSocket = new WebSocket('ws://' + window.location.host +'/'+ data.team.url +'/'+ data.channel.url);

    messageLog.scrollTop = messageLog.scrollHeight;
    message.focus();

    if (data.channel.history) {
        for (entry in data.channel.history){
            update(data.channel.history[entry]);
        }
    }

    chatSocket.addEventListener('open', function(event){
        console.log('sys:CONNECTED');
    });



    chatSocket.addEventListener('message', function(event){
        var message = JSON.parse(event.data);

        console.log(message);

        update(message);

    });


    chatSocket.addEventListener('close', function(event){
        console.log('sys:DISCONNECTED');
    });


    message.addEventListener('keypress', function(event){
        if(event.keyCode == '13' && this.value != ''){

            // send text
            send('text',this.value);
            if(event.preventDefault) event.preventDefault();
            this.value='';
        }
    });



    function send(type,data) {
        var messagePachage = {
            message: {
                type : type,
                data : data
            }
        }

        // into the ether
        chatSocket.send(JSON.stringify(messagePachage));
    }

    function update(data){

        messageBlock = document.getElementById('message-template').content.cloneNode(true);
        messageBlock.querySelector('.displayname').innerText = data.user.displayname;
        messageBlock.querySelector('.created').innerText = data.created;
        messageBlock.querySelector('.data').innerText = data.data;

        messageLog.appendChild(messageBlock);

    }


}


