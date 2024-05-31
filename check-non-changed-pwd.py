import csv,hashlib

with open("./pcc-users.csv", "r", encoding="utf-8") as csv_file:
    #リスト形式
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    
    for row in f:
        uname = hashlib.sha256(row[1].encode('utf-8')).hexdigest()
        passwd = row[5]
        
        if uname == passwd:
            print(f'{row[0]}')
