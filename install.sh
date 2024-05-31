#!/bin/bash

###############################################################################
# Create setting_files/admin_info.json before run ./install.sh in root user.  #
###############################################################################

docker image build -t pcc-rent:latest . 
docker volume create pcc-rent
docker run --name pcc-rent --restart=always -p 8080:8080 -d -v pcc-rent:/PCC-RENT -t pcc-rent:latest