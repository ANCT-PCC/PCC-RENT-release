const SERVER_ADDR = 'https://pcc-rent.nemnet-lab.net/'
const $USERLIST = document.getElementById('userlist')
const $USER_SUBMIT_BUTTON = document.getElementById('user_submit_button')

const $DELUSERLIST = document.getElementById('deluserlist')
const $USER_DELETE_BUTTON = document.getElementById('user_delete_button')

$USER_SUBMIT_BUTTON.addEventListener('click',(e)=>{

    var userlist = {content: $USERLIST.value}

    $.ajax({
        url: SERVER_ADDR+'admintools/submitusers/submit',
        type: 'POST',
        data: JSON.stringify(userlist),
        dataType: 'json',
        contentType: 'application/json'
    }).always(function(jqXHR){
        console.log(jqXHR.status)
        location.reload()
    })
})

$USER_DELETE_BUTTON.addEventListener('click',(e)=>{

    var userlist = {content: $DELUSERLIST.value}

    $.ajax({
        url: SERVER_ADDR+'admintools/submitusers/delete',
        type: 'POST',
        data: JSON.stringify(userlist),
        dataType: 'json',
        contentType: 'application/json'
    }).always(function(jqXHR){
        console.log(jqXHR.status)
        location.reload()
    })
})