
   document.addEventListener('DOMContentLoaded', () => {
    
    if (document.querySelector('#channelContainer')){
      // When form is submited to create channel run following function 
      document.querySelector('#formChannel').onsubmit = () => {
        // New form request 
        let request = new XMLHttpRequest();
        let data = new FormData();
        let channel = document.querySelector('#channel').value;

        if (channel == '') 
        {
          document.querySelector('#channelMessage').innerHTML = "This field can`t be empty!";
          return false;
        } 
        else 
        {

          data.append('channel', channel);
          request.open('POST', '/channel');
          request.send(data);
          request.onload = () => {
            let data = JSON.parse(request.responseText);

            if (data.success){
              let list = document.querySelector('#channelList');
              // Remove all channels before insert all the new one. Just in case some would be removed
              while (list.firstChild) {
                list.removeChild(list.firstChild);
              }
              // Now, for everyone create a new li tag
              for (let i = 0; i < data.channels.length ; i++){
                let elem = document.createElement('li');
                elem.className = 'channel-list-item';
                elem.innerHTML = data.channels[i]["name"];
                list.append(elem);
              }

              // Messages to show for the User
              document.querySelector('#channelMessage').innerHTML = `Your channel ${channel} has been created`;

            }else
            {
              document.querySelector('#channelMessage').innerHTML = `There was an error. ${channel} already exist`;
            }
          }
          
          return false;
        }
      }
    }
  });