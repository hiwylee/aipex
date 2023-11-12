import gradio as gr
import json
from search import RAG

rag = RAG()

def update(message, history):
    answer, source = rag.QA(message)
    print({"answer": answer, "source":source })
    print("\n-----------------------")
    # gr.json({"answer": answer, "source":source })
    return  answer 

gr.ChatInterface(update).launch(share=True, server_port=8000)
