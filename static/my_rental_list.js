const SERVER_ADDR = 'https://pcc-rent.nemnet-lab.net/'
const $logout_button = document.getElementById('logout_button');

var list = [];


/*ページ(DOM)読み込み後に実行*/
window.onload = function(){

    //tbodyのIDを取得(この中で処理します)
    var tbody = document.getElementById('item-table');

    $.ajax(
      {
        url:SERVER_ADDR+'show_my_rental_list',
        type:'GET',
        dataType: 'json',
        async: 'false'
      }).done(function(json){
        var data=JSON.stringify(json);
        var res = JSON.parse(data);

        for (i = res.length-1; i >= 0; i--){
          //tr エレメントを新規作成(ただ生成するだけ)
          var tr = document.createElement('tr');
          
          //列(td)用のループ
          for (j = 0; j < 7; j++){
              //tdエレメントをを生成
              var td = document.createElement('td');
              //tdの中に入れたいモノをセット
              if(j == 0){
                td.innerHTML = res[i]['number']
              }else if(j== 1){
                td.innerHTML = res[i]['item_name']
              }else if(j==2){
                td.innerHTML = "<a id='item"+String(i)+"'>"+res[i]['returned']+"</a>"+"<br>"+"<button id='"+"return_button"+String(i)+"' type='button' class='btn btn-primary'>返却</button>"
              }else if(j==3){
                td.innerHTML = res[i]['deadline']
              }else if(j==4){
                td.innerHTML = res[i]['rent']
              }else if(j==5){
                td.innerHTML = res[i]['use']
              }else if(j==6){
                td.innerHTML = "<a id='rental_id"+String(i)+"'>"+res[i]['rental_id']
              }
              //生成したtdをtrにセット
              tr.appendChild(td);
              
          }//列用のループ閉じ
          //tr エレメントをtbody内に追加(ここではじめて表示される)
          tbody.appendChild(tr);
  
        }//行用のループ閉じ
        
        //貸し出し中以外の表示をしている場合、ボタンを非表示に
        for(i=res.length-1;i>=0;i--){
          if(res[i]['returned'] != '貸し出し中'){
            document.getElementById('item'+String(i)).style.color = 'green'
            document.getElementById('return_button'+String(i)).style.visibility = 'hidden'
          }else if(res[i]['returned'] == '貸し出し中'){
            document.getElementById('item'+String(i)).style.color = 'orange'
          }

          document.getElementById('return_button'+String(i)).addEventListener('click',(e)=>{
            var number = e.target.id[13]
            var iteminfo = [{
              rental_id: document.getElementById("rental_id"+number).textContent
            }]
            $.ajax(
              {
                url:SERVER_ADDR+'return_item',
                type:'POST',
                data:JSON.stringify(iteminfo), //ここで辞書型からJSONに変換
                dataType: 'json',
                contentType: 'application/json'
              }).always(function(){
                location.reload()
              })
          })
        }

      }).fail(function(){
        console.log("failed")
      });

};
