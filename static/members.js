const SERVER_ADDR = 'http://localhost:8080/'
const $logout_button = document.getElementById('logout_button');


/*ページ(DOM)読み込み後に実行*/
window.onload = function(){

    //tbodyのIDを取得(この中で処理します)
    var tbody = document.getElementById('item-table');

    $.ajax(
      {
        url:SERVER_ADDR+'show_members',
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
          for (j = 0; j < 4; j++){
              //tdエレメントをを生成
              var td = document.createElement('td');
              //tdの中に入れたいモノをセット
              if(j == 0){
                td.innerHTML = res[i]['display']
              }else if(j== 1){
                td.innerHTML = res[i]['uname']
              }else if(j==2){
                td.innerHTML = res[i]['grade']+res[i]['class']
              }else if(j==3){
                td.innerHTML = "Discord: "+res[i]['discord']
              }
              //生成したtdをtrにセット
              tr.appendChild(td);
          }//列用のループ閉じ
          //tr エレメントをtbody内に追加(ここではじめて表示される)
          tbody.appendChild(tr);
  
        }//行用のループ閉じ

      }).fail(function(){
        console.log("failed")
      });

};
