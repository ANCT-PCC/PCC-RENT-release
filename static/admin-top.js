const SERVER_ADDR = 'http://localhost:8080/'
const $MOVE_DB = document.getElementById('move_db')
const $MOVE_ITEM = document.getElementById('move_item')
const $MOVE_USER = document.getElementById('move_user')

window.onload = function(){

    $MOVE_DB.addEventListener('click',(e)=>{
        window.location = SERVER_ADDR+'admintools/db'
    })
    
    $MOVE_ITEM.addEventListener('click',(e)=>{
        window.location = SERVER_ADDR+'admintools/item'
    })

    $MOVE_USER.addEventListener('click',(e)=>{
        window.location = SERVER_ADDR+'admintools/user'
    })
}