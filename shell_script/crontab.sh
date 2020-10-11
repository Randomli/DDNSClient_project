#!/bin/bash
cd /script/DDNSClient_project
source ./venv/bin/activate
cd ./bin
python check_wan_ip.py
deactivate
