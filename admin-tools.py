#未実装

main_msg = '''
    備品管理システム PCC-RENT 管理者ツール

    ***メインメニュー***

    1, 学年一括進級設定
    2, 備品の一括登録実行
    3, ユーザの一括登録実行
    4, 任意SQLの実行
    5, 終了
'''
while True:
    print(main_msg)

    main_selector = input("操作番号を入力> ")

    if main_selector == '1':
        msg1 = '''
            1が選択されました。
            学年の一括進級を設定しますか？
            ※ 5年生は「卒業扱い」となり、アカウントが無効化されます

            y: はい
            n: いいえ
        '''
        print(msg1)
        selector_1 = input("操作を入力> ")
        if selector_1 == 'y' or selector_1 == 'Y':
            selector_1_1 = input("留年者はいますか？(y/n): ")
            if selector_1_1 == 'y' or selector_1_1 == 'Y':
                ignore_uname = []
                while True:
                    uname = input("留年した人のユーザ名[例:s203120]を入力してください。\n「end」を入力するまで続けて入力できます。")
                    if uname == 'end' or uname == 'END':
                        break
                    else:
                        ignore_uname.append(uname)
                    
                for i in range(len(ignore_uname)):
                    print(ignore_uname[i])
                selector_1_2 = input("以上のユーザ名を除外して、そのほかを進級させます。(y/n)\n")
                

                if selector_1_2 == 'y' or selector_1_2 == 'Y':
                    #除外しつつ進級作業
                    pass
                else:
                    print("中止します。はじめからやり直してください。")

            else:
                #全員を進級
                print("全員を進級させます")
        else:
            print("中止します。はじめからやり直してください。")
            continue

    elif main_selector == '2':
        msg2 = '''
            2が選択されました。
            備品の一括登録を開始します。

            「itemList.csv」に以下の形式で情報を記載していることを確認してください。
            形式：備品番号,備品名,財源

            実行しますか？
            y: はい
            n: いいえ
        '''
        selector_2 = input("操作番号を入力> ")
        exit()

    elif main_selector == '3':
        msg3 = '''
            3が選択されました。
            ユーザの一括登録を開始します。

            「userList.csv」に以下の形式で情報を記載していることを確認してください。
            形式： 学年,学科,氏名,学校Gmailのメールアドレス

            実行しますか？
            y: はい
            n: いいえ
        '''
        selector_2 = input("操作番号を入力> ")
        msg3_1 = '''
            ユーザ一括登録を行いました。
            新規ユーザには、「パスワードの変更作業」をお願いしてください。
        '''
        exit()

    elif main_selector == '4':
        msg4 = '''
            4が選択されました。
            任意のSQLコマンドを実行します。
        '''
        sqlcmd = input("SQLコマンドを入力> ")
        exit()

    elif main_selector == '5':
        print("終了します。\n")
        exit()

    else:
        print("無効なオプションです。\n")