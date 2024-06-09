import dbc,hashlib

res = dbc.get_all_users()

for i in range(len(res)):
    uname = str(res[i][1])
    display = str(res[i][0])
    flag = dbc.ckpwdchange(uname=uname)
    if flag == 1:
        print(f'{display} : {flag}')
        newpwd = 'Kusopass@'+uname[1:]
        print(newpwd)
        text = hashlib.sha256(newpwd.encode('utf-8')).hexdigest()

        dbc.update_user_info(uname,'passwd',text)
    else:
        continue
