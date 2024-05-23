const SERVER_ADDR = 'https://pcc-rent.nemnet-lab.net/'
const $DB_DOUNLOAD = document.getElementById('dbdl_button');
const $SQL_EXECUTE = document.getElementById('sqlexecute_button') 
const $SQL_RESULT = document.getElementById('sqlresult')
const $SQL_CMD = document.getElementById('sqlcmd')

$DB_DOUNLOAD.addEventListener('click',(e)=>{
    window.location = SERVER_ADDR+'admintools/pcc-rent.db'
})

$SQL_EXECUTE.addEventListener('click',(e)=>{
    command = $SQL_CMD.value

    data = {
        'command': String(command)
    }

    $.ajax({
        url:SERVER_ADDR+'sqlexecute',
        type:'POST',
        data:JSON.stringify(data), //ここで辞書型からJSONに変換
        dataType: 'json',
        contentType: 'application/json'
    }).always(function(jqXHR){
        console.log(jqXHR.status)
    })
})