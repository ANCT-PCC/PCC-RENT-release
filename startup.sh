#!/bin/bash
PREV_ADDR='http://localhost:8080/'
SERVER_ADDR='https://pcc-rent.nemnet-lab.net/'

sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/login.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/admin-db.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/admin-user.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/admin-item.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/admin-top.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/admintools.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/dashboard.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/members.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/my_rental_list.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/passwd_change.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/pcc-items.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/user_settings.js

python run.py