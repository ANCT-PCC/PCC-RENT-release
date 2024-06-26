from flask import Flask, redirect, url_for, render_template, request,make_response,send_file
from flask_httpauth import HTTPDigestAuth
import dbc
import random,string
import sqlite3
import json
import hashlib
import datetime
import userSubmit,itemSubmit

TOKEN_SIZE = 64 #トークンのサイズ
COOKIE_AGE = 1 #Cookieの有効期限(単位:h)
VERSION = 'ver.2.3'

#初期化処理
def init():
    #すべてのトークンを無効化
    command='''UPDATE "pcc-users" SET accessToken = "NoToken" WHERE accessToken != "NoToken"'''
    conn = sqlite3.connect(dbc.DB_NAME)
    c = conn.cursor()
    #テーブルがなければ作成
    c.execute(dbc.INIT_SQL_COMMAND)
    c.execute(dbc.INIT_SQL_COMMAND_2)
    c.execute(dbc.INIT_SQL_COMMAND_3)
    conn.commit()
    res = dbc.sqlExecute(1,command)
    print(f"\nアクセストークン初期化を実行\n")
    print(f"Response: {res}\n\n")

#ランダムトークン生成
def randomname(TOKEN_SIZE):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=TOKEN_SIZE))

app = Flask(__name__)
app.config['SECRET_KEY'] = randomname(TOKEN_SIZE)
auth = HTTPDigestAuth()

try:
    with open('setting_files/admin_info.json','r',encoding='utf-8') as f:
     Admin = json.load(f)

except FileNotFoundError:
    print("[PCC-RENT] ERROR: setting_files/admin_info.json NOT FOUND.")
    exit()

@auth.get_password
def get_pw(id):
    return Admin.get(id)

@app.route('/',methods=['GET'])
def index():
    token = request.cookies.get('token')
    uname = request.cookies.get('uname')
    displayname = request.cookies.get('displayname')
    if token is None or uname is None or displayname is None:
        return redirect('/login')
    else:
        pwchangeFlag = dbc.ckpwdchange(uname=uname)
        if pwchangeFlag == 1:
            return redirect('/pwdchange')
        uname,login_status = dbc.cktoken(uname,token)
        if login_status == 3: #ログイン状態である
            return render_template('dashboard.html',uname = displayname,ver=VERSION)
        elif login_status == 1 or login_status == 2:
            return redirect('/login')
        
@app.route('/favicon.ico')
def favicon():
    return send_file('favicon.ico')
    

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        res = request.json[0]
        uname = res['uname']
        passwd = hashlib.sha256(res['passwd'].encode("utf-8")).hexdigest()
        
        uinfo = dbc.search_userinfo_from_name(uname)
        if len(uinfo) != 0:
            if(uinfo[0][5] == passwd):
                passwd_flag = True
            else:
                passwd_flag = False

            if passwd_flag == True: #パスワードがあっている
                token = randomname(TOKEN_SIZE=TOKEN_SIZE) #一意のトークン
                displayname = dbc.search_userinfo_from_name(uname)[0][0]
                res = make_response(redirect('/'))
                expires = int(datetime.datetime.now().timestamp()) + 60*60*COOKIE_AGE
                res.set_cookie('token', token,expires=expires)
                res.set_cookie('uname', uname,expires=expires)
                res.set_cookie('displayname',displayname,expires=expires)
                
                #DBに新しいトークンを上書きと同時に
                #サブプロセスでタイマーを作動
                dbc.update_token(uname,token)

            else:
                token="Nodata"
                uname="Nodata"
                return "444",444
        else:
            token="Nodata"
            uname="Nodata"
            if res == "Nodata" or token is None or res is None:

                return "444",444 #ログインエラーのレス
            else:
                uname , login_sta = dbc.cktoken(uname,str(token))
                
                if(login_sta == 3):
                    pass
                elif(uname == "Not Submit"):
                    return "446",446 #ユーザ登録なし
                elif(login_sta == 2):
                    #return "445",445 #トークンが無効
                    pass
                
        return res
    
    elif request.method == 'GET':
        uname = request.cookies.get('uname')
        token = request.cookies.get('token')
        if token is None:
            return render_template('login.html')
        else:
            uname,login_sta = dbc.cktoken(uname,token)
            if login_sta == 1 or login_sta==2 or login_sta==0:
                return render_template('login.html')
            elif login_sta == 3:
                return redirect('/')

@app.after_request
def set_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Method'] = 'GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS'  # noqa: E501
    response.headers['Access-Control-Allow-Headers'] = 'Content-type,Accept,X-Custom-Header'  # noqa: E501
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Max-Age'] = '86400'
    return response

@app.route('/logout')
def logout():
    uname=request.cookies.get('uname')
    res=make_response(redirect('/login'))
    res.delete_cookie('token')
    res.delete_cookie('uname')
    res.delete_cookie('displayname')
    dbc.update_token(uname,'NoToken')

    return res

@app.route('/user_settings',methods=['GET','POST'])
def user_settings():

    if request.method == 'POST':
        uname = request.cookies.get('uname')
        token = request.cookies.get('token')

        uname,login_status = dbc.cktoken(uname,token)
        if login_status != 3:
            return redirect('/login')
        else:
            currentPWD = hashlib.sha256(request.json[0]['currentPWD'].encode("utf-8")).hexdigest()
            newPWD = hashlib.sha256(request.json[0]['newPWD'].encode("utf-8")).hexdigest()

            uinfo = dbc.search_userinfo_from_name(uname)
            if uinfo[0][5] != currentPWD:
                return "444",444
            elif uinfo[0][5] == currentPWD:
                #パスワード変更処理
                previnfo,newinfo = dbc.update_user_info(uname,'passwd',newPWD)
                newuinfo = dbc.search_userinfo_from_name(uname)
                return "415",415


    else:

        uname = request.cookies.get('uname')
        token = request.cookies.get('token')
        displayname = request.cookies.get('displayname')

        uname,login_status = dbc.cktoken(uname,token)
        if login_status != 3:
            return redirect('/login')
        else:
            return render_template('user_settings.html',uname=displayname,ver=VERSION)
        
@app.route('/pwdchange')
def pwdchange():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')
    displayname = request.cookies.get('displayname')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        return render_template('passwd_change.html',uname=displayname,ver=VERSION)
        
@app.route('/user_settings_discord',methods=['POST'])
def user_settings_discord():
    
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        newDiscord = request.json[0]['newDiscord']
        uinfo = dbc.search_userinfo_from_name(uname)
        #Discordのユーザ名変更処理
        previnfo,newinfo = dbc.update_user_info(uname,'discord',newDiscord)
        return "OK",200
    
@app.route('/my_rental_list')
def my_rental_list():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')
    displayname = request.cookies.get('displayname')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        flag = dbc.ckpwdchange(uname)
        if flag == 1:
            return redirect('/pwdchange')
        return render_template('my_rental_list.html',uname=displayname,ver=VERSION)
    
@app.route('/pcc-items')
def pcc_items():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')
    displayname = request.cookies.get('displayname')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        flag = dbc.ckpwdchange(uname)
        if flag == 1:
            return redirect('/pwdchange')
        return render_template('pcc-items.html',uname=displayname,ver=VERSION)
    
@app.route('/members')
def members():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')
    displayname = request.cookies.get('displayname')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        flag = dbc.ckpwdchange(uname)
        if flag == 1:
            return redirect('/pwdchange')
        return render_template('members.html',uname=displayname,ver=VERSION)
    
@app.route('/show_members')
def show_members():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        res = dbc.get_all_users()
        member_info = []

        for flag in range(len(res)):
            dict = {}
            dict['display']=str(res[flag][0])
            dict['uname']=str(res[flag][1])
            dict['grade']=str(res[flag][9])
            dict['class']=str(res[flag][10])
            dict['discord']=str(res[flag][11])
            member_info.append(dict)

        return json.dumps(member_info)
    
@app.route('/show_my_rental_list')
def show_my_rental_list():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')
    displayname = request.cookies.get('displayname')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        res = dbc.sarch_rent_items(displayname)
        rental_info = []

        for flag in range(len(res)):
            dict = {}
            dict['number']=str(res[flag][0])
            dict['item_name']=str(res[flag][1])
            dict['use']=str(res[flag][2])
            dict['rent']=str(res[flag][4])
            dict['deadline']=str(res[flag][5])
            dict['returned']=str(res[flag][6])
            dict['rental_id']=str(res[flag][7])
            rental_info.append(dict)

        return json.dumps(rental_info)
    
@app.route('/show_all_rental_list')
def show_all_rental_list():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        res = dbc.get_rent_items()
        rental_info = []

        for flag in range(len(res)):
            dict = {}
            dict['number']=str(res[flag][0])
            dict['item_name']=str(res[flag][1])
            dict['use']=str(res[flag][2])
            dict['rentby']=str(res[flag][3])
            dict['rent']=str(res[flag][4])
            dict['deadline']=str(res[flag][5])
            dict['returned']=str(res[flag][6])
            rental_info.append(dict)

        return json.dumps(rental_info)
    
@app.route('/show_all_rental_history')
def show_all_rental_history():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        res = dbc.get_rent_history()
        rental_info = []

        for flag in range(len(res)):
            dict = {}
            dict['number']=str(res[flag][0])
            dict['item_name']=str(res[flag][1])
            dict['use']=str(res[flag][2])
            dict['rentby']=str(res[flag][3])
            dict['type']=str(res[flag][4])
            dict['timestamp']=str(res[flag][5])
            dict['deadline']=str(res[flag][6])
            rental_info.append(dict)

        return json.dumps(rental_info)
    
@app.route('/show_pcc-items')
def show_pcc_items():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        res = dbc.get_all_items()
        item_info = []

        for flag in range(len(res)):
            dict = {}
            dict['number']=str(res[flag][0])
            dict['item_name']=str(res[flag][1])
            dict['desc']=str(res[flag][2])
            dict['resource']=str(res[flag][3])
            dict['rental']=str(res[flag][4])
            dict['picture']=str(res[flag][5])
            item_info.append(dict)

        return json.dumps(item_info)
    
@app.route('/return_item',methods=['POST'])
def return_item():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        rental_id = request.json[0]['rental_id']
        userinfo = dbc.search_userinfo_from_name(uname)[0]
        displayname = userinfo[0]
        
        res = dbc.return_item(rental_id=rental_id,returnedby=displayname+' '+uname)
        if res == 0:
            return "OK",200
        else:
            return "ERROR",400
        
@app.route('/rental_item',methods=['POST'])
def rental_item():
    uname = request.cookies.get('uname')
    token = request.cookies.get('token')
    displayname = request.cookies.get('displayname')

    uname,login_status = dbc.cktoken(uname,token)
    if login_status != 3:
        return redirect('/login')
    else:
        item_number = request.json[0]['item_number']
        item_name = dbc.search_iteminfo_from_number(item_number)[1]
        use = '未記載'
        res = dbc.rent_item(item_number,item_name,use,displayname,uname)

        if res == 0:
            return "OK",200
        else:
            return "ERROR",400
        
@app.route('/admintools')
@auth.login_required
def admintools_top():
    return redirect('/admintools/top')

@app.route('/admintools/<string:page>')
@auth.login_required
def admintools(page):
    return render_template('admintools/'+page+'.html',ver=VERSION)

@app.route('/admintools/pcc-rent.db')
@auth.login_required
def admintools_dlfile():
    #dlname = 'pcc-rent'+datetime.datetime.now().strftime('%Y%m%d%H%M')+'.db'
    #mimetype='application/octet-stream'
    #dir = os.path.abspath(__file__)[:-7]
    return send_file('pcc-rent.db',as_attachment=True)

@app.route('/admintools/submitusers/<string:mode>',methods=['POST'])
@auth.login_required
def submitusers(mode):
    if mode == 'submit':
        submit_contents = str(request.json['content'])
        with open('userList.csv','w',encoding='utf-8') as f:
            f.write(submit_contents)

        userSubmit.userSubmit()
        return "OK"
    elif mode == 'delete':
        delete_contents = str(request.json['content'])
        with open('deluserList.csv','w',encoding='utf-8') as f:
            f.write(delete_contents)
        
        userSubmit.userDelete()
    

@app.route('/admintools/submititems/<string:mode>',methods=['POST'])
@auth.login_required
def submititems(mode):

    if mode == 'submit':
        submit_contents = str(request.json['content'])
        with open('itemList.csv','w',encoding='utf-8') as f:
            f.write(submit_contents)

        itemSubmit.itemSubmit()
        return "OK"
    elif mode == 'delete':
        delete_contents = str(request.json['content'])
        with open('delitemList.csv','w',encoding='utf-8') as f:
            f.write(delete_contents)

        itemSubmit.itemDelete()
        return "OK"
    else:
        return "404",404
    
@app.route('/admintools/db/sqlexecute',methods=['POST'])
@auth.login_required
def sqlexecute():
    sqlcmd = str(request.json['sqlcmd'])
    result = dbc.sqlExecute(True,sqlcmd)
    data = {'content':result}
    print(data['content'])
    return data['content'],200


init()
print("Access: http://localhost:8080/")
#app.run(port=443,host="0.0.0.0",debug=True,ssl_context=context,threaded=True)
app.run(port=8080,host="0.0.0.0",debug=True,threaded=True)