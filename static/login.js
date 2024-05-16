const $login_button = document.getElementById("loginbutton");
const $form_email = document.getElementById("floatingInput");
const $form_passwd = document.getElementById("floatingPassword");
const $login_status_error = document.getElementById("login_status_error");

const SERVER_ADDR='https://pcc-rent.nemnet-lab.net/'

$login_status_error.style.visibility = "hidden";


$login_button.addEventListener('click',(e) => {
    if ($form_email.value == '' || $form_passwd.value == ''){
        $login_status_error.textContent = 'ユーザ名/パスワードを入力してください';
        $login_status_error.style.visibility = 'visible';
    }else{
    var form_data = [
        {uname: String($form_email.value),
        passwd: String($form_passwd.value)
    }
    ];    

    console.log(form_data)
    
    $.ajax(
        {
          url:'https://pcc-rent.nemnet-lab.net/'+'login',
          type:'POST',
          data:JSON.stringify(form_data), //ここで辞書型からJSONに変換
          dataType: 'json',
          contentType: 'application/json'
    }).always(function (jqXHR) {
        console.log("statuscode::")
        console.log(jqXHR.status);
        if(String(jqXHR.status) === "200"){
            //ログイン続行
            login_status_error.style.visibility = "hidden";
            window.location.href = 'https://pcc-rent.nemnet-lab.net/';
        }else if(String(jqXHR.status) === "444"){
            //入力の修正を求める
            login_status_error.textContent = "ユーザ名/パスワードに誤りがあります。code="+jqXHR.status;
            login_status_error.style.visibility = "visible";
        }else if(String(jqXHR.status) === "445"){
            login_status_error.textContent = "トークンが無効です code="+jqXHR.status;
            login_status_error.style.visibility = "visible";
        }else if(String(jqXHR.status) === "446"){
            login_status_error.textContent = "ユーザ登録がありません code="+jqXHR.status;
            login_status_error.style.visibility = "visible";
        }else if(String(jqXHR.status) === "447"){
            login_status_error.textContent = "正常に処理できませんでした code="+jqXHR.status;
            login_status_error.style.visibility = "visible";
        }else{
            //入力の修正を求める
          login_status_error.textContent = "不明なエラー。システム管理者へ問い合わせてください";
          login_status_error.style.visibility = "visible";
        }
    });
    }

});