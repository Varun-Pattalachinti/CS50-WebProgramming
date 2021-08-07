//need to show all channels
document.addEventListener('DOMContentLoaded',()=>{
  if(localStorage.getItem('username'))
  {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    const channelNames = Handlebars.compile(document.querySelector('#seeallchannelsscript').innerHTML);
    //emit for the channel names
    socket.emit('channelNamesRequired!')

    if(localStorage.getItem('selectedChannel') )
    {
      console.log("got here")
      socket.emit('channelSelected!',{'channel_name':localStorage.getItem('selectedChannel'),'username':localStorage.getItem('username')})
    }
    //if channelsUpdated emitted by the server
    socket.on('channelsUpdated!', function(channels){
          channels = channels['channels']
          document.querySelector('#channellist').innerHTML = channelNames({'channels':channels});
          document.querySelectorAll(".selectchannel").forEach((channel)=>{channel.addEventListener('submit',function(e){
            channelName = e.currentTarget.id
            //alert(channelName) //works
            socket.emit('channelSelected!',{'channel_name':channelName,'username':localStorage.getItem('username')})
            localStorage.setItem('selectedChannel',channelName)

            e.preventDefault()
          })})
      });
  }

});
