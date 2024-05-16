import dbc,csv

csvfile = open("userList.csv","r",encoding="utf-8")

file = csv.reader(csvfile, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

for row in file:
    dbc.create_new_user(display_name=row[2],name=row[3][:7],email=row[3],isAdmin=False,passwd=row[3][:7],grade=row[0],user_class=row[1],discord='未設定')

csvfile.close()