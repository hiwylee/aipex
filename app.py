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



# https://hwangtoemat.github.io/computer-science/2020-10-21-CORS/
# CORS(app, resources={r'*': {'origins': 'apex server'}})

app = Flask(__name__)
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

import time
if __name__ == "__main__":
    print("Ready...!")
    app.run(debug=True, host='0.0.0.0', port=8000)
