#!/bin/bash
# source ../.apex_genai/bin/activate
date
VIRTUAL_ENV="/home/opc/.apex_genai"
export VIRTUAL_ENV

$VIRTUAL_ENV/bin/python -c 'import sys; print(sys.version_info)'

cd /home/opc/aipex

# remove db lock if exists because only one local QDrant allowed
# 
rm ./db_23c/.lock 2> /dev/null

export FLASK_ENV=development
export FLASK_APP=app
$VIRTUAL_ENV/bin/python app.py
date
