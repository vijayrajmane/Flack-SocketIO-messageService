import os
import datetime
from flask import Flask, render_template, redirect, jsonify, request, url_for, session
from flask_socketio import SocketIO, emit, send
from flask_session import Session
from channel import Channel

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
socketio = SocketIO(app)
Session(app)

channels=[]

@app.route("/")
def index():
    try:
        #Render template with session name if session is already created
        return render_template("index.html", name=session["name"], lastChannel=session["lastChannel"], channels=channels)
    except KeyError:
        try:
            return render_template("index.html", name=session["name"], channels=channels)
        except KeyError:
            return render_template("index.html", channels=channels)

# Creating session for name entered and returning status
@app.route("/name",methods=["POST"])
def name():
    
    name = request.form.get("name")
    
    if name is not None:
        session["name"]=name
        return jsonify(
           {
                "success": True,
                    "name": name
            }
        )
    else:
        return jsonify(
            {
                "success": False
            }
        )


@app.route("/lastChannel", methods=["POST"])
def lastChannel():
    #Remember Last Channel visited in Session
    channel = request.form.get("lastChannel")
    session["lastChannel"] = channel
    return '', 204

@app.route("/channel",methods=["POST"])
def channel():
    channel = request.form.get('channel')
    
    # Check if channel already exists 
    for elem in channels:
        if channel in elem.name:
            return jsonify({"success": False})

    # If no channel with same name exists create channel
    newChannel = Channel(channel)
    channels.append(newChannel)

    # Create a dictionary for every object so then can be tranformed easily into JSON objects
    channelsFeed = []
    for object in channels:
        channelsFeed.append(object.__dict__)

    return jsonify(
                        {
                            "success": True, 
                            "channel": channel, 
                            "channels": channelsFeed
                         }
                    )           

@app.route("/delete",methods=["POST"])
def delete():
    channel = request.form.get('channel')   # channel from which message is to be deleted
    message = request.form.get('message')   # message to be deleted

    for x in channels:
        # check is channel is in channels[]
        if x.name == channel:   
            for y in x.messages:
                # check message that we want to delete from that channel
                if y["message"]==message:
                    # Message found then delete
                    del(x.messages[x.messages.index(y)])
    return '', 204

@socketio.on("sendMessage")
def chat(data):
    channel = data["channel"]
    message = data["message"]
    #Checking for an existing channel with that same name
    for checkChannel in channels:
        # If exist then append the new message 
        if checkChannel.name == channel:
            time = '{:%H:%M:%S}'.format(datetime.datetime.now())
            sender = session["name"]
            checkChannel.newMessage(message, sender, channel, time)

            last_message = checkChannel.messages[-1]
            emit("update", last_message, broadcast=True)
            return
    # if channel doesn't exists emit a Not success message
    emit("update", 'Not success', broadcast=True)

@socketio.on("update")
def conect(data):
    channel = data["channel"]
    #Checking for an existing channel with that same name
    for checkChannel in channels:
        # If exist, charge all old messages stored there and emit
        if checkChannel.name == channel:
            oldMessages = checkChannel.messages
            name = session["name"]
            emit("updateChat", (oldMessages, name), broadcast=True)
            return
    # Else, emit a notFound message
    emit("updateChat", 'notFound', broadcast=True)

if __name__ == '__main__':
    socketio.run(app)                 