#!/bin/bash

date
VIRTUAL_ENV="/home/opc/py3.11"
export VIRTUAL_ENV

$VIRTUAL_ENV/bin/python -c 'import sys; print(sys.version_info)'

cd /home/opc/dev

rm ./db/.lock 2> /dev/null
export FLASK_ENV=development
export FLASK_APP=app
$VIRTUAL_ENV/bin/python app.py
date
