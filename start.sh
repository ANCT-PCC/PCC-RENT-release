#!/bin/bash

sleep 5s
source /home/ubuntu/PCC-RENT-release/.venv/bin/activate
screen -AdmS pcc-rent python run.py
