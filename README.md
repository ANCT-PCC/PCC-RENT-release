# PCC-RENT パソコン部備品管理システム

メモ  
---
**test.py:**  
書いて字の如く。  
**main.py:**  
 メインロジック  
**dbc.py:**  
 DB操作用自作ライブラリ  
**itemManager.py:**  
 アイテムマネージャー(CLI)  
**login.py:**  
CLIでのログインスクリプト  
**pcc-rent.db:**  
このシステムの核となる存在。データ喪失から**死守**せよ

## 環境
MacBook Air 13 (Apple M2)  
macOS Sonoma 14  
Python 3.10.11  
モジュール: req.txt参照  

## インストール  
python3.10 -m venv .venv  
source ./.venv/bin/activate  
pip install -r req.txt  
userSubmit.csvとitemSubmit.csvに内容を記述してから  
./userSubmit.sh  
./itemSubmit.sh  
./start.sh