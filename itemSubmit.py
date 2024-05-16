import dbc,csv

csvfile = open("itemList.csv","r",encoding="utf-8")

file = csv.reader(csvfile, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

print("ファイルをロードしました。")


flag =0
for row in file:
    if(flag == 0):
        flag+=1
        continue
    else:
        dbc.create_new_item(number=row[0],name=row[1],desc="未設定",resource=row[2],rental='なし',picture='なし')
        flag+=1

csvfile.close()