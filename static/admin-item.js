const SERVER_ADDR = 'https://pcc-rent.nemnet-lab.net/'
const $ITEMLIST = document.getElementById('itemlist')
const $ITEM_SUBMIT_BUTTON = document.getElementById('item_submit_button')

const $DELITEMLIST = document.getElementById('delitemlist')
const $ITEM_DELETE_BUTTON = document.getElementById('item_delete_button')

$ITEM_SUBMIT_BUTTON.addEventListener('click',(e)=>{

    var itemlist = {content: $ITEMLIST.value}

    $.ajax({
        url: SERVER_ADDR+'admintools/submititems/submit',
        type: 'POST',
        data: JSON.stringify(itemlist),
        dataType: 'json',
        contentType: 'application/json'
    }).always(function(jqXHR){
        console.log(jqXHR.status)
        location.reload()
    })
})

$ITEM_DELETE_BUTTON.addEventListener('click',(e)=>{

    var itemlist = {content: $DELITEMLIST.value}

    $.ajax({
        url: SERVER_ADDR+'admintools/submititems/delete',
        type: 'POST',
        data: JSON.stringify(itemlist),
        dataType: 'json',
        contentType: 'application/json'
    }).always(function(jqXHR){
        console.log(jqXHR.status)
        location.reload()
    })
})