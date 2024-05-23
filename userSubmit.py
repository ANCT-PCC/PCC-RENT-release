import dbc,csv

def userSubmit():
    csvfile = open("userList.csv","r",encoding="utf-8")

    file = csv.reader(csvfile, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

    for row in file:
        dbc.create_new_user(display_name=row[2],name=row[3][:7],email=row[3][:7]+'@edu.asahikawa-nct.ac.jp',isAdmin=False,passwd=row[3][:7],grade=row[0],user_class=row[1],discord='未設定')

    csvfile.close()

def userDelete():
    csvfile = open("deluserList.csv","r",encoding="utf-8")

    file = csv.reader(csvfile, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

    for row in file:
        dbc.delete_user(row[0])
        
    csvfile.close()

if __name__ == '__main__':
    userSubmit()