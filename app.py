from flask import Flask, request, Response ,jsonify #,render_template
from flask_restx import Resource, Api, Namespace
from flask_restx import fields
from flask_cors import CORS
from search import RAG
import json

from wiki_search import wiki_search
from rag_search import rag_search
from summarize_api import do_summarize_api
from generate_api import do_generate_api

import dotenv

# from flask_restplus import field

# do it first


app = Flask(__name__)

# https://hwangtoemat.github.io/computer-science/2020-10-21-CORS/
# CORS(app, resources={r'*': {'origins': 'apex server'}})

CORS(app)
api = Api(app)

ns = Namespace("hello")

api.add_namespace(ns,'/hello')
api.add_namespace(wiki_search,'/api/v1/wiki_search')
api.add_namespace(rag_search,'/api/v1/rag_search')
api.add_namespace(do_summarize_api,'/api/v1/summarize')
api.add_namespace(do_generate_api,'/api/v1/generate')

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res

"""
rag = RAG()

# https://givemethesocks.tistory.com/116

questition_model = api.model('generate', strict=True, model={
    'question': fields.String(title='question', default='What was Reed College great at?', required=True),
})

summary_model = api.model('summary', strict=True, model={
    'question': fields.String(title='text to summmary', default='text to summmary', required=True),
})

classify_model = api.model('classify', strict=True, model={
    'question': fields.String(title='lists to classify', default='list to classify', required=True),
})
"""

@api.route('/hello')  
class DoGet(Resource):
    def get(self):  
        return {'hello': 'world!'}

"""
# rest api 
@api.route('/api/v1/generate')  
class Generate(Resource):
    @api.expect(questition_model, validate=True)
    def post(self):  
        question = request.json.get('question')
        answer, source = rag.QA(question)
        setQuestion(question, answer,source )
        # return jsonify(ai_answer)

        return ai_answer

@api.route('/api/v1/summarize')
class Summarize(Resource):
    @api.expect(summary_model, validate=True)
    def post(self):
        question = request.json.get('question')
        answer, source = rag.QA(question)
        setQuestion(question, answer, source)

        return ai_answer

@api.route('/api/v1/classify')
class Classfy(Resource):
     
     @api.expect(classify_model, validate=True)
     def post(self):
        question = request.json.get('question')
        answer, source = rag.QA(question)
        setQuestion(question, answer, source)

        return ai_answer
        #return json.dumps(ai_answer)
"""

import time
if __name__ == "__main__":
    print("Ready...!")
    app.run(debug=True, host='0.0.0.0', port=8000)
