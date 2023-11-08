OCI Generative AI :  python version 3.9.x

Requires-Python >=3.7,<3.10
oci==2.112.1+preview.1.1649
----------------------------
.env

# [OCI | COHERE]
EMBED_TYPE="OCI"
LLM_TYPE="OCI"
service_endpoint="https://generativeai.aiservice.us-chicago-1.oci.oraclecloud.com"
# your compartment_id
compartment_id="ocid1.tenancy.oc1..aaaaaaaasz6cicsgfbqh6tj3xahi4ozoescfz36bjm3kucc7lotk2oqep47q"

----------------------------
To create a virtual environment using venv:

$ python3.11 -m venv py3.11
$ source py3.11/bin/activate
$ pip install -r requirements.txt
# -- 추가 package 설치 후 
$ pip freeze > requirements.txt

$ deactivate


firewall-cmd --zone=public --add-port=8080/tcp  
firewall-cmd --zone=public --add-port=8000/tcp  
firewall-cmd --zone=public --add-port=443/tcp --permanent
sudo firewall-cmd --runtime-to-permanent

1.3 check

sudo firewall-cmd --zone=public --list-all


1.4 requirements.txt file 추가
whl/genai_langchain_integration-0.1.5-py3-none-any.whl
whl/oci-2.112.1+preview.1.1649-py3-none-any.whl

----------------------------------------
1.5 oci setup config
----------------------------------------

[DEFAULT]
user=ocid1.user.oc1..aaaaaaaak4x2p2vk33n7vehr6udqx6it7zp6pezoch6v7dky5smxyzy3vg4q
fingerprint=ca:b2:c7:fd:06:1e:fe:a7:bb:7e:48:3b:96:05:b6:a2
key_file=/Users/wylee/.oci/oci_api_key.pem
tenancy=ocid1.tenancy.oc1..aaaaaaaa6ma7kq3bsif76uzqidv22cajs3fpesgpqmmsgxihlbcemkklrsqa
region=us-chicago-1

----------------------------------------
1.6 소스 반영
----------------------------------------
from genai_langchain_integration.langchain_oci import OCIGenAI
from genai_langchain_integration.langchain_oci_embeddings import OCIGenAIEmbeddings

source : compartment_id 변경
llm = OCIGenAI(
    model_id="cohere.command", 
    service_endpoint="https://generativeai.aiservice.us-chicago-1.oci.oraclecloud.com",
    compartment_id="ocid1.tenancy.oc1..aaaaaaaasz6cicsgfbqh6tj3xahi4ozoescfz36bjm3kucc7lotk2oqep47q",
    temperature=0.0
)

embeddings = OCIGenAIEmbeddings(
    model_id="cohere.embed-english-light-v2.0", 
    service_endpoint="https://generativeai.aiservice.us-chicago-1.oci.oraclecloud.com",
    compartment_id="ocid1.tenancy.oc1..aaaaaaaasz6cicsgfbqh6tj3xahi4ozoescfz36bjm3kucc7lotk2oqep47q"
)

----------------------------------------

1.5 테스트

http://152.70.251.41/api/v1/generate

- api request
{
   "question": "What did the author liken The Whole Earth Catalog to?"
}

- api response
{
    "question": question,
    "answer" :  answer,
    "source" :  source
}

------ api docs ---------
from flask_restx import fields

questition_model = api.model('query', strict=True, model={
    'question': fields.String(title='question', default='What was Reed College great at?', required=True),
})

class Generate(Resource):
    """
	swagger api doc 
	"""
    @api.expect(questition_model, validate=True)
    def post(self):  
        question = request.json.get('question')
        answer, source = rag.QA(question)
        setQuestion(question, answer,source )
        # return jsonify(ai_answer)

        return ai_answer
---------api.doc(POST/PUT) , api.expect -------------------
my_model = api.model('MyModel', {
    'name': fields.String(description='The name', required=True),
    'type': fields.String(description='The object type', enum=['A', 'B']),
    'age': fields.Integer(min=0),
})


class Person(fields.Raw):
    def format(self, value):
        return {'name': value.name, 'age': value.age}


@api.route('/my-resource/<id>', endpoint='my-resource')
@api.doc(params={'id': 'An ID'})
class MyResource(Resource):
    @api.doc(model=my_model)
    def get(self, id):
        return {}

    @api.doc(model=my_model, body=Person)
    def post(self, id):
        return {}
		
## input data model
summarize_model = do_summarize_api.model('summarize', strict=True, model={
    #'style': fields.List(fields.String(),title='summary style', default=style, required=True),
    'style': fields.String(title='summary style', default='|'.join(style), required=True),
    'srcipts': fields.String(title='call scripts to summarize', default=scripts, required=True),
})
class DoSummarize(Resource) :
    @do_summarize_api.expect(summarize_model, validate=True)
    def post(self) :
	....		
----- api gateway ------
backend response timeout : 60 초
--> api gateway
------- api gateway --------
backend response timeout : 60 초
Reading response timeout in seconds : 60 초
-> api gateway에서 CORS Policy에서 Origin, Methods, Headers 모두 * 처리


Path prefix: /aipex

/generate http://152.70.251.41/api/v1/generate
/rag_search. http://152.70.251.41/api/v1/rag_search
/wiki_search http://152.70.251.41/api/v1/wiki_search
/summarize   http://152.70.251.41/api/v1/summarize

https://cexcieoazb3u2spa76p7z5xyn4.apigateway.ap-seoul-1.oci.customer-oci.com/aipex/generate
https://cexcieoazb3u2spa76p7z5xyn4.apigateway.ap-seoul-1.oci.customer-oci.com/aipex/rag_search
https://cexcieoazb3u2spa76p7z5xyn4.apigateway.ap-seoul-1.oci.customer-oci.com/aipex/wiki_search
https://cexcieoazb3u2spa76p7z5xyn4.apigateway.ap-seoul-1.oci.customer-oci.com/aipex/summarize
https://cexcieoazb3u2spa76p7z5xyn4.apigateway.ap-seoul-1.oci.customer-oci.com/aipex/hello

------- CORS ---------
# https://hwangtoemat.github.io/computer-science/2020-10-21-CORS/
# CORS(app, resources={r'*': {'origins': 'apex server'}})
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return resƒ
----------------------------------------------------

---------import name 'ChatCohere error---------------
(py3.11) [opc@instance-20230720-0227 dev]$ python summerize_api.py 
Traceback (most recent call last):
  File "/home/opc/dev/summerize_api.py", line 3, in <module>
    from langchain.chat_models import ChatCohere
ImportError: cannot import name 'ChatCohere' from 'langchain.chat_models' (/home/opc/py3.11/lib64/python3.11/site-packages/langchain/chat_models/__init__.py)

pip install --upgrade langchain

--

