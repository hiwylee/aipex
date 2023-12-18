from flask import request
from flask_restx import  Namespace,Resource
from flask_restx import fields

from search import RAG
import json


import json

rag = RAG()

do_generate_api = Namespace('generate')
do_generate_api_model = do_generate_api.model('generate', strict=True, model={
    'question': fields.String(title='keyword to search', default='What was Reed College great at?', required=True),
})


@do_generate_api.route('/')
class Generate(Resource):
    @do_generate_api.expect(do_generate_api_model, validate=True)
    def post(self):  
        question = request.json.get('question')
        answer, source = rag.QA(question)

        return { 
            "question": question, 
            "answer" :  answer,
            "source" :  source
            }
    