const SERVER_ADDR = 'https://pcc-rent.nemnet-lab.net/'
const $logout_button = document.getElementById('logout_button');


/*ページ(DOM)読み込み後に実行*/
window.onload = function(){

    //tbodyのIDを取得(この中で処理します)
    var tbody = document.getElementById('item-table');

    $.ajax(
      {
        url:SERVER_ADDR+'show_pcc-items',
        type:'GET',
        dataType: 'json',
        async: 'false'
      }).done(function(json){
        var data=JSON.stringify(json);
        var res = JSON.parse(data);

        for (i = 0; i < res.length; i++){
          //tr エレメントを新規作成(ただ生成するだけ)
          var tr = document.createElement('tr');
          //列(td)用のループ
          for (j = 0; j < 6; j++){
              //tdエレメントをを生成
              var td = document.createElement('td');
              //tdの中に入れたいモノをセット
              if(j == 0){
                td.innerHTML = "<a id='item_number"+String(i)+"'>"+res[i]['number']+"</a>"
              }else if(j== 1){
                td.innerHTML = res[i]['item_name']
              }else if(j==2){
                td.innerHTML = res[i]['desc']
              }else if(j==3){
                td.innerHTML = "<a id='resource"+String(i)+"'>"+res[i]['resource']+"</a>"
              }else if(j==4){
                td.innerHTML = res[i]['rental']+'<br>'+"<button id='rental_button"+String(i)+"' type='button' class='btn btn-primary'>借りる</button>"
              }else if(j==5){
                td.innerHTML = res[i]['picture']
              }
              //生成したtdをtrにセット
              tr.appendChild(td);
          }//列用のループ閉じ
          //tr エレメントをtbody内に追加(ここではじめて表示される)
          tbody.appendChild(tr);
  
        }//行用のループ閉じ

        for(i=0;i<res.length;i++){
          if(res[i]['rental'] != 'なし'){
            document.getElementById('rental_button'+String(i)).style.visibility = 'hidden';
          }
          if(res[i]['resource'] == '金庫'){
            document.getElementById('resource'+String(i)).style.color = 'green';
          }else{
            document.getElementById('resource'+String(i)).style.color = 'red';
          }

          document.getElementById('rental_button'+String(i)).addEventListener('click',(e)=>{
            var number = e.target.id[13]
            var iteminfo = [{
              item_number: document.getElementById("item_number"+number).textContent
            }]
            $.ajax(
              {
                url:SERVER_ADDR+'rental_item',
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
