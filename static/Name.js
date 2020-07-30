
document.addEventListener('DOMContentLoaded', () => { 

    if (document.querySelector('#formDisplay'))
    {   //On submitting name run following function
        document.querySelector('#formDisplay').onsubmit = ()=>{
            //create Http request
            let request = new XMLHttpRequest();

            let name = document.querySelector('#name').value;
            let data = new FormData;
            data.append('name',name);
            //open request for /name route in application.py
            request.open('POST', '/name');
            request.send(data)

            request.onload = ()=>
            {   //After getting response parse it
                let data = JSON.parse(request.responseText);
                // if success=True
                if(data.success)
                {
                    document.querySelector('#form').style.display='none';
                    let header = document.createElement('h2');
                    header.className = 'text-center'
                    header.innerHTML = 'Welcome '+ data.name;

                    document.querySelector('#DisplayName').append(header);
                    document.querySelector('#channelContainer').style.display = '';
                    document.querySelector('#user-data').dataset.username = data.name;

                }
                else
                {
                    document.querySelector('#DisplayName').innerHTML='Error Occured!!, Please try again :(';
                }
            }
            return false;
        }
    }
});