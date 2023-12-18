conda create -n aipex  python=3.11
conda activate aipex
cd aipex/
pip install --upgrade pip


pip install -r  requirements-local.txt 


## app.sh
---------------------------------------
# conda activate aipex_genai
VIRTUAL_ENV="/home/opc/miniconda3/envs/aipex"
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
---------------------------------------