from flask import request
from flask_restx import Resource, Api, Namespace,fields
#import json
import dotenv
import weaviate
import os


wiki_search = Namespace('wiki_search')
cohere_api_key = os.getenv("COHERE_API_KEY")


wiki_model = wiki_search.model('wiki', strict=True, model={
    'question': fields.String(title='keyword to search', default='역대 최고 흥행 영화 3 개', required=True),
})

# Connect to the Weaviate demo databse containing 10M wikipedia vectors
# This uses a public READ-ONLY Weaviate API key

dotenv.load_dotenv(".env")
weaviate_api_key=os.getenv("WEAVIATE_API_KEY")

auth_config = weaviate.auth.AuthApiKey(api_key=weaviate_api_key) 
client = weaviate.Client(
    url="https://cohere-demo.weaviate.network/",
    auth_client_secret=auth_config,
    additional_headers={
        "X-Cohere-Api-Key": cohere_api_key,
    }
)

if(client.is_ready()) :
    print("weaviate is ready")
else :
    print("weaviate is not ready")

@wiki_search.route('/')
class WikiPost(Resource) :
    @wiki_search.expect(wiki_model, validate=True)
    def post(self) :
        question = request.json.get('question')
        query_result = semantic_serch(question, results_lang='ko')
        if query_result is None :
            return ({"error" : f'no data founc for query [{question}]'},400)
        print_result(query_result)
        return query_result
    
    #@wiki.expect(wiki_model, validate=True)
    def get(self) :
        # question = request.json.get('question')

        question = "time travel plot twist"
        query_result = semantic_serch(question, results_lang='ko')

        # Print out the result
        print_result(query_result)
        return query_result
    

def semantic_serch(query, results_lang=''):
    """ 
    Query the vectors database and return the top results. 


    Parameters
    ----------
        query: str
            The search query
            
        results_lang: str (optional)
            Retrieve results only in the specified language.
            The demo dataset has those languages:
            en, de, fr, es, it, ja, ar, zh, ko, hi

    """
    
    nearText = {"concepts": [query]}
    properties = ["text", "title", "url", "views", "lang", "_additional {distance}"]
    print(f'wikipidea query : {query}, lang : {results_lang} ')
    # To filter by language
    if results_lang != '':
        where_filter = {
        "path": ["lang"],
        "operator": "Equal",
        "valueString": results_lang
        }
        response = (
            client.query
            .get("Articles", properties)
            .with_where(where_filter)
            .with_near_text(nearText)
            .with_limit(5)
            .do()
        )
        
    # Search all languages
    else:
        response = (
            client.query
            .get("Articles", properties)
            .with_near_text(nearText)
            .with_limit(5)
            .do()
        )

    print(f'wikipea query result is {response}')
    result = response['data']['Get']['Articles']
    if result is None :
        print(f'wikipea query result is null - response->data->Get->Articles')
    return result

def print_result(result):
    """ Print results with colorful formatting """
    for item in result:
        print(f"\033[95m{item['title']} ({item['views']}) {item['_additional']['distance']}\033[0m")
        print(f"\033[4m{item['url']}\033[0m")
        print(item['text'])
        print()