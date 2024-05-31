const SERVER_ADDR = 'http://localhost:8080/'
const $logout_button = document.getElementById('logout_button');
const $changePWD_button = document.getElementById('changePWD_button');
const $changeSuccess = document.getElementById('changeSuccess');
const $changeFailed = document.getElementById('changeFailed');
const $newPWD = document.getElementById('newPWD');
const $newPWD_retype = document.getElementById('newPWD_retype');
const $currentPWD = document.getElementById('currentPWD');

function init(){
  $changeFailed.style.visibility = 'hidden';
  $changeSuccess.style.visibility = 'hidden';
  $currentPWD.value = '';
  $newPWD.value = '';
  $newPWD_retype.value = '';
};

$changePWD_button.addEventListener('click',(e)=>{
  currentPWD = $currentPWD.value;
  newPWD = $newPWD.value;
  newPWD_retype = $newPWD_retype.value;

  if (newPWD != newPWD_retype){
    $changeSuccess.style.visibility = 'hidden';
    $changeFailed.innerText = "新しいパスワードが一致しません";
    $changeFailed.style.visibility = 'visible';

    $currentPWD.value = '';
    $newPWD.value = '';
    $newPWD_retype.value = '';
  }else{
    var passwd_array = [{
      currentPWD: String(currentPWD),
      newPWD: String(newPWD)
    }];

    $.ajax(
      {
        url:SERVER_ADDR+'user_settings',
        type:'POST',
        data:JSON.stringify(passwd_array), //ここで辞書型からJSONに変換
        dataType: 'json',
        contentType: 'application/json'
    }).always(function(jqXHR){
      if (jqXHR.status == "415"){
        $changeFailed.style.visibility = 'hidden';
        $changeSuccess.innerText = "パスワードが変更されました code="+jqXHR.status;
        $changeSuccess.style.visibility = 'visible';

        $currentPWD.value = '';
        $newPWD.value = '';
        $newPWD_retype.value = '';
      }else if(jqXHR.status == "444"){
        $changeSuccess.style.visibility = 'hidden';
        $changeFailed.innerText = "現在のパスワードが間違っています。code="+jqXHR.status;
        $changeFailed.style.visibility = 'visible';

        $currentPWD.value = '';
        $newPWD.value = '';
        $newPWD_retype.value = '';
      }else{
        $changeSuccess.style.visibility = 'hidden';
        $changeFailed.innerText = "不明なエラー。code="+jqXHR.status;
        $changeFailed.style.visibility = 'visible';

        $currentPWD.value = '';
        $newPWD.value = '';
        $newPWD_retype.value = '';
      }
    });
  };
  
});


init()