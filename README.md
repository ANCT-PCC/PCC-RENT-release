# PCC-RENT パソコン部備品管理システム

## メモ
**run.py:**  
PCC-RENTのAPIサーバ本体  
**dbc.py:**  
 DB操作用自作ライブラリ   
**pcc-rent.db:**  
このシステムの核となる存在。データ喪失から**死守**せよ

## 開発環境
コンテナエンジン: Docker Engine 26.1.3  
イメージおよび使用言語: Python3.10  
Pythonモジュール: req.txt参照  

## 想定動作環境  
Ubuntu Server 22.04  
Docker Engine 26.1.3

## インストール  
新規インストール手順  
1, https://qiita.com/NeK/items/d9431d5cdfa16dffe6dc に従ってdocker Engineを入れる  
2, git clone <URL>  
3, chmod +rx install.sh uninstall.sh reinstall.sh update.sh startup.sh  
4, ./install.sh  
5, 必要に応じてCloudflare Tunnnelのコネクタをdockerを用いて生やす  
6, 動作確認  

## 更新
更新手順  
1, "URL"/admin_toolsからデータベースファイルをダウンロード  
2, docker stop pcc-rent  
3, git pull  
4, ./reinstall.sh  
5, pcc-rentにアクセスして動作確認  