from flask import request
from flask_restx import  Namespace,Resource
from flask_restx import fields

from search import RAG
import json


import json

rag = RAG()

rag_search = Namespace('rag_search')
rag_search_model = rag_search.model('rag', strict=True, model={
    'question': fields.String(title='keyword to search', default='What was Reed College great at?', required=True),
})


@rag_search.route('/')
class Generate(Resource):
    @rag_search.expect(rag_search_model, validate=True)
    def post(self):  
        question = request.json.get('question')
        answer, source = rag.QA(question)

        return { 
            "question": question, 
            "answer" :  answer,
            "source" :  source
            }
    