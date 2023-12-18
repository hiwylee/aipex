import streamlit as st
import json
import pandas as pd

from search import RAG

rag = RAG()

st.title("manual semantic search")


exam = st.selectbox('Example',
                       ("Oracle 23c new features",
                        "what is blockchain table and new feature of oracle database 23c related to blockchain", 
                        "Make a list of database 23c innovations in AI", 
                        "Make a list of database 23c innovations in AI",
                        "Are there features related to Machine Learning in Oracle Database 23c?"),
                    )
kw = st.text_input('질문', placeholder="what is JSON Relational Duality", value=exam)  

btn = st.button('문서검색') 

st.divider()  # 👈 Draws a horizontal rule
if btn :
    answer, source = rag.QA(kw)
    # print({"answer": answer, "source":source })
    # st.text_area("answer",value=answer)
    st.json({"answer": answer })
    
    st.json({source})

