import streamlit as st
from send_post import do_post
import pandas as pd


st.title("위키 다국어 검색")

lang_sz, kw_sz, btn_sz = st.columns([0.1,0.6,0.3])
with lang_sz :
    lang = st.selectbox('언어',
                       ('ko','en', 'de', 'fr', 'es', 'it', 'ja', 'ar', 'zh', 'hi'))
with kw_sz :
    kw = st.text_input('키워드', placeholder="키워드를 입력하세요", value="역대 최고 흥행 영화 3 개")  

with btn_sz :
    btn = st.button('다국어 검색') 

st.divider()  # 👈 Draws a horizontal rule
if btn :
    res = do_post("/aipex/wiki_search",{"question": kw, "lang":lang })  

    sorted_df = pd.read_json(res.text).sort_values(by='views',ascending=False)
    df = sorted_df.drop(columns=['lang','_additional','text'])
    st.dataframe(
        df,
        column_config={
            "title": "제목",
            "url": st.column_config.LinkColumn("URL"),
            "views":  st.column_config.NumberColumn(  "조회", format="%d ⭐",)
            }
        )

    st.divider()  # 👈 Draws a horizontal rule   
    st.json(res.text)