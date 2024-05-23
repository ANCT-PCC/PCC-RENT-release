const SERVER_ADDR = 'https://pcc-rent.nemnet-lab.net/'
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