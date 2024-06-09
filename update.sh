#!/bin/bash

rm ../pcc-rent-Backup/pcc-rent.db
rm -r ../pcc-rent-Backup/setting_files
rm -r ../pcc-rent-Backup
mkdir ../pcc-rent-Backup
docker cp pcc-rent:/PCC-RENT/pcc-rent.db ../pcc-rent-Backup
docker cp pcc-rent:/PCC-RENT/setting_files ../pcc-rent-Backup
echo "****Use GitHub Account which joined ANCT-PCC Organization !****"
git pull
docker cp ../pcc-rent-Backup/pcc-rent.db pcc-rent:/PCC-RENT
docker cp ../pcc-rent-Backup/setting_files pcc-rent:/PCC-RENT
./reinstall.sh