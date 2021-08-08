import os

from flask import Flask
from flask_socketio import SocketIO, emit

from flask import request
from flask import render_template,redirect
from flask import jsonify

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
channel_names = {}
channel_recent_msg = {}
#need to create queue of top 100 messages later
def initChannel(channel_name):
    if channel_name in channel_names:
        return False
    channel_names[channel_name] = True
    channel_recent_msg[channel_name] = []
    return True

def sortChannels(channel_names):
    """
    sort the channels alphabetically and return array
    """
    return sorted(channel_names.keys())
@app.route("/", methods = ["GET","POST"])
def index():

    #need to have a button that initsChannels in userpage.html
    #need to implement websockets so that change can be emitted to all users dont like this implementation
    """
    if request.method == "POST":
        if 'newChannelButton' in request.form:
            #based on name attribute of input
            new_channel_name = request.form.get("channelName")
            if len(new_channel_name) == 0 :
                #redundancy will also make input required
                return render_template("userpage.html", channels = channel_names_arr, msg = "Please Enter A Channel Name")
            if initChannel(new_channel_name) == -1:
                return render_template("userpage.html",channel_names_arr, msg = "Channel name already taken!")
            if initChannel(new_channel_name) == 1:
                #SUCCESS!
                channel_names_arr = sortChannels(channel_names)
                return render_template("userpage.html",channels = channel_names_arr, msg = "Channel successfully added!")
    channel_names_arr = sortChannels(channel_names)
    """
    return render_template("userpage.html")

@socketio.on("channelNamesRequired!")
def get_channel_names():
    channels = sortChannels(channel_names)
    emit('channelsUpdated!',{'channels':channels,'isModified':True},broadcast=True)

@socketio.on("AddChannel!")
def add_channel(channel_name):
    if initChannel(channel_name['channel_name']) == True:
        channels = sortChannels(channel_names)
        username =channel_name['username']
        emit('channelsUpdated!',{'channels':channels, 'isModified':True, 'username':username}, broadcast = True)
    else:
        channels = sortChannels(channel_names)
        username =channel_name['username']
        emit('channelsUpdated!',{'channels':channels, 'isModified' :False,'username':username}, broadcast = True)

@socketio.on("channelSelected!")
def channel_selected(channel_name_json):
    channel_name = channel_name_json['channel_name']
    username = channel_name_json['username']
    #get all messages corresponding to the channel
    emit('RecentMsgs!',{'channel_name': channel_name,'recent_messages':channel_recent_msg[channel_name],'username':username}, broadcast=True)

@socketio.on("AddMessage!")
def add_message(add_message_json):
    channel_name = add_message_json['channel_name']
    message = []
    username = add_message_json['username']
    message_text = add_message_json['message']
    message.append(username)
    message.append(message_text)
    print(message)
    print(channel_names)
    print(channel_recent_msg[channel_name])
    channel_recent_msg[channel_name].append(message)
    if(len(channel_recent_msg[channel_name]) >= 100):
        channel_recent_msg[channel_name] = channel_recent_msg[channel_name][1:]
    emit('RecentMsgs!',{'channel_name':channel_name,'recent_messages':channel_recent_msg[channel_name],'username': username}, broadcast = True)
    #create username and save to localhost if completely new user
    #otherwise display username saved in localhost this needs to be done in javascript tho....
