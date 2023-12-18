cd
cd aipex
rm ./db_23c/.lock 2> /dev/null
STREAMLIT_SERVER_HEADLESS=true python -m streamlit run search_ui2.py --server.port=8000
