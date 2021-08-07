document.addEventListener('DOMContentLoaded',()=>{
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  //alert("got here")
  const channelMsgs = Handlebars.compile(document.querySelector('#displaychannelmsgsscript').innerHTML);
  //console.log(channelMsgs())
  socket.on('RecentMsgs!', function(channel_msgs_json){
    msgs = channel_msgs_json["recent_messages"]
    if(msgs.length > 0 & channel_msgs_json["username"] === localStorage.getItem('username'))
    {
        document.querySelector("#displaychannelmsg").innerHTML = channelMsgs({'message':channel_msgs_json["recent_messages"]})
    }
    if( msgs.length === 0 & channel_msgs_json["username"] === localStorage.getItem('username'))
    {
      document.querySelector("#displaychannelmsg").innerHTML = channelMsgs({'message':['There are no messages yet for this Channel']})
    }
    if(channel_msgs_json["username"] === localStorage.getItem('username'))
    {
      const addMessage = Handlebars.compile(document.querySelector('#addmessagescript').innerHTML)
      document.querySelector("#addmessage").innerHTML = addMessage()

      document.querySelector("#addmessageform").addEventListener('submit',function(e){
        e.preventDefault()
      })

      document.querySelector("#submitmessage").addEventListener('click', function(e){
        addmessage_ = document.querySelector("#addmessagetext").value
        channel_name = channel_msgs_json["channel_name"]
        socket.emit('AddMessage!',{'channel_name':channel_name, 'username':localStorage.getItem("username"),'message':addmessage_})
      })
    }


  });
})
