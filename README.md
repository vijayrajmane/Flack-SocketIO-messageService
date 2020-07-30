
In this project I have created an web app called Flack which is online message service.
SocketIO is used for real time chat. This is a one page application. Javascript is used to run server-side code.
In this app where user has to enter the name which is associated with message in chats and will be remembered even after closing the browser.
User has to create a channel as long as it doen't conflict name with other channel. After creating channel it is add to channel list.
On clicking on channel chat window for that channel is opened.
Mesaage send by user is associated with timestamp and name.
User can delete its own message by clicking delete button which is visible if you hover over the message.
----------

Name.js: Creating display name if not created before

Channel.js : Create a new channel

index.html : One page app so only one html file. It contains all html code and also contain javascript code which is for using to send message using socket.

Personal Touch
My personal touch in this project was to implement the option of deleting your own messages. Delete button appears if you move cursor on your message. On clicking it will delete message.