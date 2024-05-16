import sqlite3,json,datetime
import random,string
import json
import subprocess
import hashlib

DB_NAME = 'pcc-rent.db'
TOKEN_SIZE = 64
WEBHOOK_URL = 'https://discord.com/api/webhooks/1238851270597541888/krtdLGswv7LRx1KhqvQdRh2MR9xCGsSSROmoRikxD_FEeQ3gfU16OUzB1CPSko5OZDX9'

INIT_SQL_COMMAND = '''CREATE TABLE IF NOT EXISTS "pcc-users"(display,name,email,isAdmin,solt,passwd,activate_flag,uuid,accessToken,grade,class,discord) '''
INIT_SQL_COMMAND_2 = '''CREATE TABLE IF NOT EXISTS "pcc-items"(number,item_name,desc,resource,rental,picture,rental_id) '''
INIT_SQL_COMMAND_3 = '''CREATE TABLE IF NOT EXISTS "pcc-rental"(number,item_name,use,rentby,rent,deadline,returned,rental_id) '''

#汎用SQL実行
def sqlExecute(mode:bool,sql:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(sql)
    res=c.fetchall()

    if mode == True:
        #書き込みモード
        print("\n[Notice]\t書き込みモードで実行しました")
        conn.commit()
    else:
        print("\n[Notice]\t書き込みモードで実行していません")
        pass

    conn.close()
    return res

def discord_message(message:str,uname:str):
    command = ["python","send_discord.py",message,uname]
    subprocess.Popen(command)
    

#################################################################

#ユーザー関連

#################################################################

#新規ユーザを作成する
def create_new_user(display_name:str,name:str,email:str,isAdmin:bool,passwd:str,grade:int,user_class:str,discord:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    #テーブルがなければ作成
    c.execute(INIT_SQL_COMMAND)
    solt = 'not set'

    data = (display_name,name,email,str(isAdmin),solt,hashlib.sha256(passwd.encode("utf-8")).hexdigest(),0,'not set','NoToken',str(grade)+'年 ',user_class,discord)
    #テーブルに登録情報を記録
    sql = f'''
        INSERT INTO "pcc-users" VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
        EXCEPT
        SELECT * FROM "pcc-users" WHERE name == '{name}'
        '''
    c.execute(sql,data)
    #コミット(変更を反映)
    conn.commit()
    c.close()
    return 0

#ユーザーを削除
def delete_user(name:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    #ユーザー削除
    c.execute(f'''DELETE FROM "pcc-users" WHERE name == "{name}" ''')
    conn.commit()
    c.close()

#ユーザー登録情報を検索(ユーザー名から)
def search_userinfo_from_name(name:str):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    c.execute(f'''SELECT * FROM "pcc-users" WHERE name == "{name}" ''')
    res = c.fetchall()
    #レコードのフォーマット↓
    #display,name,email,isAdmin,solt,passwd,activate_flag,uuid
    conn.close()
    return res #ユーザーのレコードを配列として返す

#全ユーザー登録情報一覧
def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    sql = '''
        SELECT * FROM "pcc-users"
    '''
    c.execute(sql)
    res = c.fetchall()
    return res #ユーザー登録情報を配列として返す

#ユーザー登録情報更新
def update_user_info(old_uname:str,column:str,new_data:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    prev_userinfo = search_userinfo_from_name(old_uname)

    sql1 = f'''
        UPDATE "pcc-users" SET "{column}" = "{new_data}" WHERE name = "{old_uname}"
    '''
    c.execute(sql1)
    conn.commit()
    
    new_userinfo = search_userinfo_from_name(old_uname)

    return prev_userinfo,new_userinfo

#有効なトークンの有効性検証結果とユーザ名の応答
def cktoken(name:str,token:str):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    #ユーザの登録有無
    c.execute(f'''SELECT * FROM "pcc-users" WHERE name == "{name}" ''')
    suser_res = c.fetchall()
    
    #トークンがすでに存在しているか
    c.execute(f'''SELECT * FROM "pcc-users" WHERE accessToken == "{token}" ''')
    token_res = c.fetchall()

    #ログインが正しいか
    c.execute(f'''SELECT * FROM "pcc-users" WHERE name == "{name}" AND accessToken == "{token}"''')
    usr_token_res = c.fetchall()
    #レコードのフォーマット↓
    #name,email,isAdmin,solt,passwd,activate_flag,uuid,accessToken
    conn.close()

    if len(suser_res) == 0:
        #ユーザ登録なし
        return "Not Submit" ,0
    else:
        if len(token_res) == 0 : #ほかにログインしている可能性あり
            #nameが存在かつ、NoTokenではないTokenが存在
            #print("ヒットなし")
            return name,1
        elif str(token_res[0][8]) == "NoToken": #ログインなし/トークンの期限切れ
            #nameが存在かつ、NoTokenである
            #print("トークンなし")
            return "NoUname",2
        else:#ユーザのトークンが有効(ログイン状態である)
            name = token_res[0][1]
            #トークンの時間制限をリセットする処理を書きたい
            return str(name),3

#トークン更新
def update_token(uname:str,new_token:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql1 = f'''
        UPDATE "pcc-users" SET accessToken = "{new_token}" WHERE name = "{uname}"
    '''
    c.execute(sql1)
    conn.commit()




#################################################################

#備品関連

#################################################################

#備品を登録する
def create_new_item(number:str,name:str,desc:str,resource:str,rental:str,picture:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    #テーブルがなければ作成
    c.execute(INIT_SQL_COMMAND_2)
    data = (number,name,desc,resource,rental,picture,'NoSet')
    #テーブルに登録情報を記録
    sql = f'''
        INSERT INTO "pcc-items" VALUES(?,?,?,?,?,?,?)
        EXCEPT
        SELECT * FROM "pcc-items" WHERE number == '{number}'
        '''
    c.execute(sql,data)
    #コミット(変更を反映)
    conn.commit()
    c.close()
    return 0

#備品を削除
def delete_item(number:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    #備品削除
    c.execute(f'''DELETE FROM "pcc-items" WHERE number == '{number}' ''')
    conn.commit()
    c.close()

#備品を検索(名前から)
def search_iteminfo_from_name(name:str):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    res =[]
    for i in c.execute(f'''SELECT * FROM "pcc-items" WHERE item_name == '{name}' '''):
        res = json.loads(json.dumps(i,ensure_ascii=False))
    conn.close()
    return res #備品のレコードを配列として返す

#備品を検索(備品番号から)
def search_iteminfo_from_number(number:str):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    res =[]
    for i in c.execute(f'''SELECT * FROM "pcc-items" WHERE number == '{number}' '''):
        res = json.loads(json.dumps(i,ensure_ascii=False))
    conn.close()
    return res #備品のレコードを配列として返す

#ユーザの貸し出し備品を検索(備品番号から)
def search_userrentalinfo_from_number(number:str):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    res =[]
    c.execute(f'''SELECT * FROM "pcc-rental" WHERE number == '{number}' ''')
    res = c.fetchall()
    conn.close()
    return res #備品のレコードを配列として返す
    

#備品を借用(履歴に記録)
def rent_item(item_number:str,item_name:str,use:str,rentby:str,uname:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    #テーブルがなければ作成
    c.execute(INIT_SQL_COMMAND_3)
    #res =[]
    c.execute(f'''SELECT * FROM "pcc-rental" WHERE number == '{item_number}' AND returned == '貸し出し中' AND rental_id == 'NotSet' ''')
    res = c.fetchall()

    print(len(res))
    if len(res)==0:
        sql = f'''
            INSERT INTO "pcc-rental" VALUES(?,?,?,?,?,?,?,?)
        '''
        timestamp = datetime.datetime.now()
        deadline = timestamp + datetime.timedelta(days=14)
        rental_id = ''.join(random.choices(string.ascii_letters + string.digits, k=TOKEN_SIZE))
        data = (item_number,item_name,use,rentby,timestamp.strftime('%Y年%m月%d日 %H:%M'),deadline.strftime('%Y年%m月%d日'),'貸し出し中',rental_id)
        c.execute(sql,data)
        sql2 = f'''
            UPDATE "pcc-items" SET rental = '{rentby}' WHERE number = '{item_number}'
        '''
        sql3 = f'''
            UPDATE "pcc-items" SET rental_id = '{rental_id}' WHERE number = '{item_number}'
        '''
        c.execute(sql2)
        c.execute(sql3)
        conn.commit()
        conn.close()

        #Discord 借用通知
        message = f"備品番号{item_number}:「{item_name}」を **借用** しました"
        
        userinfo = search_userinfo_from_name(uname)[0]
        grade_class = userinfo[9]+userinfo[10]
        displayname = userinfo[0]
        discord_message(message,grade_class+" "+displayname)

        return 0
    else:
        print(f"借用が重複している可能性があります: {item_number}")
        conn.commit()
        conn.close()

        return -1

#備品を返却(履歴に記録)
def return_item(rental_id:str,returnedby:str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.datetime.now()
    c.execute(f'''SELECT * FROM "pcc-rental" WHERE rental_id = "{rental_id}"''')
    info = c.fetchall()
    c.execute(f'''UPDATE "pcc-rental" SET returned = '返却済み:<br>{timestamp.strftime('%Y年%m月%d日 %H:%M')}' WHERE rental_id == '{rental_id}' ''')
    
    sql3 = f'''
        UPDATE "pcc-items" SET rental = 'なし' WHERE rental_id = '{rental_id}'
    '''
    sql4 = f'''
        UPDATE "pcc-items" SET rental_id = 'NoSet' WHERE rental_id = '{rental_id}'
    '''
    c.execute(sql3)
    c.execute(sql4)
    conn.commit()
    conn.close()

    #Discord 返却通知
    item_number = info[0][0]
    item_name = info[0][1]
    message = f"備品番号{item_number}: 「{item_name}」を **返却** しました"
    discord_message(message,returnedby)

    return 0

#借りられている備品を検索
def get_rent_items():
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    sql = '''
        SELECT * FROM "pcc-rental"
    '''
    c.execute(sql)
    res = c.fetchall()
    return res #備品登録情報を配列として返す

#ユーザが借りている備品を検索
def sarch_rent_items(uname:str):
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    sql = f'''
        SELECT * FROM "pcc-rental" WHERE rentby == "{uname}"
    '''
    c.execute(sql)
    res = c.fetchall()
    return res #備品登録情報を配列として返す

#全備品登録情報一覧
def get_all_items():
    conn = sqlite3.connect(DB_NAME)
    c=conn.cursor()
    sql = '''
        SELECT * FROM "pcc-items"
    '''
    c.execute(sql)
    res = c.fetchall()
    return res #備品登録情報を配列として返す