from flask import request
from flask_restx import Resource, Api, Namespace,fields

## Extract Data From Calls & Video Transcripts/Interviews
from langchain.chat_models import ChatCohere
from langchain.embeddings import CohereEmbeddings
# Summarizer we'll use for Map Reduce
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.schema import Document

from flask_cors import CORS

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate, # I included this one so you know you'll have it but we won't be using it
    HumanMessagePromptTemplate
)

# To create our chat messages
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from dotenv import load_dotenv
import os

# Namespace
do_summarize_api = Namespace('summarize')

# for default value
scripts = 'text to summarize'
if os.path.isfile('acme_co.txt'):
    with open('acme_co.txt', 'r') as file:
        scripts = file.read()

style = ["one_sentence","bullet_points","short","long"]    

## input data model
summarize_model = do_summarize_api.model('summarize', strict=True, model={
    #'style': fields.List(fields.String(),title='summary style', default=style, required=True),
    'style': fields.String(title='summary style', default='|'.join(style), required=True),
    'content': fields.String(title='call scripts to summarize', default=scripts, required=True),
})

@do_summarize_api.route('/')
class DoSummarize(Resource) :
    # https://flask-restx.readthedocs.io/en/latest/swagger.html
    # my_model = api.model('MyModel', {
    #    'name': fields.String(description='The name', required=True),
    #    'type': fields.String(description='The object type', enum=['A', 'B']),
    #    'age': fields.Integer(min=0),
    # })
    # class Person(fields.Raw):
    # def format(self, value):
    #    return {'name': value.name, 'age': value.age}
    #
    # POST and PUT methods, use the body keyword 
    # @api.doc(model=my_model, body=Person)
    @do_summarize_api.expect(summarize_model, validate=True)
    def post(self) :
        style_req = request.json.get('style')
        if __debug__:
            print(f'request.json.get("style") = {style_req}')
            
        content = request.json.get('content')
        if content is None or style_req is None  :
            return ({"error" : f'request body format invalid '},400)
        
        if style_req not in style :
            print(f"parameter style = {style_req} not allow")
            return ({"error" : f'parameter style = {style_req} not allow ({style})'},400)
        output = do_summarize(content, style_req)
        if output is None  :
            return ({"error" : f'no summary data [{content}]'},400)
        return {'summary':output, 'style':style_req, 'content':content}
    
def do_summarize (content :str, user_input="one_sentence" ) -> str:
    
    load_dotenv()
    cohere_api_key=os.getenv('COHERE_API_KEY')

    if __debug__:
        print ("Transcript:\n")
        print(user_input)
        print(content) # Why 215? Because it cut off at a clean line
         # Why 215? Because it cut off at a clean line

    
    # Split our documents so we don't run into token issues.
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "\t"], chunk_size=10000, chunk_overlap=3000)
    texts = text_splitter.create_documents([content])
    if __debug__:
        print (f"You have {len(texts)} texts")
        print (f">>>\n{texts[0].page_content[0:300]}\n ")

    summary_output_options = {
        'one_sentence' : """
        - Only one sentence
        """,
        
        'bullet_points': """
        - Bullet point format
        - Separate each bullet point with a new line
        - Each bullet point should be concise
        """,
        
        'short' : """
        - A few short sentences
        - Do not go longer than 4-5 sentences
        """,
        
        'long' : """
        - A verbose summary
        - You may do a few paragraphs to describe the transcript if needed
        """
    }
    template1="""

    summarize information from given content easy for high school student to understand .
    Your goal is to write a summary from the perspective of sales rep that will highlight key points that will be relevant to making a sale
    Do not respond with anything outside of the content. If you don't know, say, "I don't know"
    """
    system_message_prompt_map = SystemMessagePromptTemplate.from_template(template1)

    human_template="{text}" # Simply just pass the text as a human message
    human_message_prompt_map = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt_map = ChatPromptTemplate.from_messages(messages=[system_message_prompt_map, human_message_prompt_map])   
    
  # You are a helpful assistant that helps {sales_rep_name}, a sales rep at {sales_rep_company}, 
    template="""

    summarize information from given content easy for high school student to understand .
    Your goal is to write a summary from the perspective of  sales rep  that will highlight key points that will be relevant to making a sale
    Do not respond with anything outside of the content. If you don't know, say, "I don't know"

    Respond with the following format
    {output_format}

    """
    system_message_prompt_combine = SystemMessagePromptTemplate.from_template(template)

    human_template="{text}" # Simply just pass the text as a human message
    human_message_prompt_combine = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt_combine = ChatPromptTemplate.from_messages(messages=[system_message_prompt_combine, human_message_prompt_combine])

    llm = ChatCohere(temperature=0,  cohere_api_key=cohere_api_key)
    chain = load_summarize_chain(
                    llm=llm,
                    chain_type="map_reduce",
                    map_prompt=chat_prompt_map,
                    combine_prompt=chat_prompt_combine,
                    #verbose=True 
                    )
    
    if user_input is None:
        user_selection = 'one_sentence'
    else:
        user_selection = user_input
    print(f'user_selection = {user_selection}')
    output = chain.run({
                        "input_documents": texts,
                        #"sales_rep_company": "Marin Transitions Partner", \
                        #"sales_rep_name" : "Greg",
                        "output_format" : summary_output_options[user_selection]
                    })
    if __debug__:
        print (output)

    print(f' ouput type = {type(output)}')
    return output

if __name__ == "__main__":
    with open('acme_co.txt', 'r') as file:
        content = file.read()
    do_summarize (content, 'short')
    if __debug__ :
        print(" Loading...")
    import sys



