import dbc,time


menustr = """
        1, 新規備品登録
        2, 備品情報の編集
        3, 備品の登録削除
        4, 備品一覧の表示

        0, 終了
    """

while True:
    print("PCC-RENT アイテムマネージャー(CLI)")
    print(menustr)
    selection = input("> ")

    if(selection == "1"):
        #新規備品登録
        print("新規備品登録")
        item_name = input("備品名を入力 > ")
        item_num = input("備品番号を入力 > ")
        item_desc = input("備品の説明文を入力 > ")
        item_source = input("財源を選択\n1,学生会部費など\n2,金庫からの出費\n> ")
        item_user = " - "
        item_pic = " - "

        dbc.create_new_item(name=item_name,number=item_num,desc=item_desc,resource=item_source,user=item_user,pic=item_pic)

        print("登録完了\n\n\n")
        res = dbc.search_iteminfo_from_name(item_name)

        if(item_source == "1"):
            source = "学生会部費など"
        elif(item_source == "2"):
            source = "金庫からの出費"
        else:
            source = "その他の財源"
        print(f"備品名:{item_name}\n備品番号:{item_num}\n説明:{item_desc}\n財源:{source}\n")

        time.sleep(3)

    elif(selection == "2"):
        #備品情報編集
        print("備品情報の編集")
        print("! この機能はまだ実装していません !")

    elif(selection == "3"):
        #備品の登録削除
        print("備品の登録削除")
        
        dbc.delete_item(input("削除する備品名 > "))
        print("削除完了")
        time.sleep(3)

    elif(selection == "4"):
        #備品一覧の表示
        print("備品一覧の表示")

        res = dbc.get_all_items()
        print("==========")
        for i in res:
            print(i)

        print("==========")

    else:
        break