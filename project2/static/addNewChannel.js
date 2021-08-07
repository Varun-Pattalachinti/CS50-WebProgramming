document.addEventListener('DOMContentLoaded',()=>{
  if(localStorage.getItem('username'))
  {
    //if the addNewChannelbutton is clicked
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    const addNewChannel = Handlebars.compile(document.querySelector('#addchannelscript').innerHTML);
    document.querySelector('#addchannel').innerHTML = addNewChannel();
    const form = document.querySelector('#addform');
    // Stop the form from submitting when a button is pressed
    form.addEventListener('submit', function(e) {
      e.preventDefault();
    });

    const submitAddChannel = document.querySelector('#submitchannelname');
    submitAddChannel.addEventListener('click',()=>{
      const channelName = document.querySelector('#channelname');
      socket.emit('AddChannel!',{'channel_name':channelName.value, 'username': localStorage.getItem('username')})
    });

    socket.on('channelsUpdated!',function(channels) {
      if(!channels['isModified'] & (channels['username'] === localStorage.getItem('username')))
      {
        alert("The channel name requested already exists. Choose another channel name.");
      }
    });

  }
});
