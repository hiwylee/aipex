from langchain.embeddings.cohere import CohereEmbeddings
from langchain.llms import Cohere

from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA
from langchain.vectorstores import Qdrant
from langchain.document_loaders import TextLoader,PyPDFLoader,CSVLoader,JSONLoader
from qdrant_client import QdrantClient

# OCI Generative AI Services
from genai_langchain_integration.langchain_oci import OCIGenAI
from genai_langchain_integration.langchain_oci_embeddings import OCIGenAIEmbeddings


import textwrap as tr
import random
import dotenv
import os
import json
import re

import oci
import logging

# Enable debug logging
logging.getLogger('oci').setLevel(logging.DEBUG)

class RAG:
    """
    RAG Class 
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):         #  클래스 객체에 _instance 속성이 없다면
            if __debug__ :
                print("__new__ is called\n")
            cls._instance = super().__new__(cls)  #  클래스의 객체를 생성하고 Foo._instance로 바인딩
        return cls._instance         

    def __init__(self):
        self._name = 'RAG'
        self._db   = None
        self._db_path   = './db'
        self._collection_name='my_documents'

        self._qa   = None
        self._llm   = None

        dotenv.load_dotenv(".env")

        self._cohere_api_key = os.getenv("COHERE_API_KEY")
        self.EMBED_TYPE   = os.getenv("EMBED_TYPE")
        self.LLM_TYPE   = os.getenv("LLM_TYPE")
        self.service_endpoint=os.getenv("service_endpoint")
        self.compartment_id=os.getenv("compartment_id")

        if not os.path.exists(self._db_path):
            if __debug__ :
                print(f"Creating DB directory {self._db_path}..\n")
            os.makedirs(self._db_path)

        self._embeddings = self.__init_embeddings__()
        self._llm = self.__init_llm__()
        # should not initialized vectordb here for loading

        
        self._prompt = self.__init_prompt()
        if __debug__ :
            print("__init__ is called\n")

    #def __str__(self):
    #    return f'str : {self._name} '

    def __init_prompt(self):
        if __debug__ :
            print("Init prompt ...\n")
        prompt_template = """Text: {context}
Question: {question}
Answer the question based on the text provided. If the text doesn't contain the answer, reply that the answer is not available."""

        return PromptTemplate( template=prompt_template, input_variables=["context", "question"])

    def __init_embeddings__(self):
        if __debug__ :
            print(f'Init embeddings EMBED_TYPE = [{self.EMBED_TYPE}]...\n')
            print(self.EMBED_TYPE)
       

        if self.EMBED_TYPE == "OCI":
            return OCIGenAIEmbeddings(
                    # model_id="cohere.embed-english-light-v2.0", 
                    model_id="cohere.embed-english-light-v2.0", 
                    service_endpoint=self.service_endpoint,
                    compartment_id=self.compartment_id,
                    )
        else :
            return  CohereEmbeddings(model = "multilingual-22-12", cohere_api_key=self._cohere_api_key)
            return  CohereEmbeddings(model = "multilingual-22-12", cohere_api_key=self._cohere_api_key)
    def __init_llm__(self):
        if __debug__ :
            print(f'Init LLM TYPE = [{self.LLM_TYPE}] ...\n')
            print(self.LLM_TYPE)
        if self.LLM_TYPE == "OCI" :
            return OCIGenAI(
                    #model_id="cohere.command", 
                    model_id="cohere.command-light", 
                    service_endpoint=self.service_endpoint,
                    compartment_id=self.compartment_id,
                    temperature=0.0
                    )
        else :
            return Cohere(model="command-nightly", temperature=0,cohere_api_key=self._cohere_api_key) 
    def __init_vectordb__(self):
        if __debug__ :
            print("Init vector db  ...\n")
        if self._db is None :
            client =  QdrantClient(path=self._db_path) 
            self._db =  Qdrant(client, self._collection_name, self._embeddings)
        if __debug__ :
            print("initialized   ...\n")
        return self._db

    
    def __loader__(self, file):
        if file.endswith('.txt'):
            return TextLoader(file)
        elif file== 'answers.json' :
            return TextLoader(file)
        elif file.endswith('.csv'):
            return TextLoader(file)
        elif file.endswith('.pdf'):
            return PyPDFLoader(file)
        elif file.endswith('.json'):
            return JSONLoader(file)
        else :
            raise ValueError(f'{file} : no loader found for the type')
    #
    # do some post processing on text
    #
    def post_process(self, splits):
        for split in splits:
            # replace newline with blank
            split.page_content = split.page_content.replace("\n", " ")
            split.page_content = re.sub("[^a-zA-Z0-9 \n\.]", " ", split.page_content)
            # remove duplicate blank
            split.page_content = " ".join(split.page_content.split())

        return splits
    
    def loadTxt(self, file):
        embeddings = self._embeddings
        if __debug__ :
            print(f"Loading File [{file}]...\n")
        ldr = self.__loader__(file)
        documents = ldr.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        texts = self.post_process(texts)
        
        Qdrant.from_documents(
                texts, 
                self._embeddings, 
                path=self._db_path, 
                collection_name=self._collection_name,
                distance_func="Dot")
        '''

        self._db.add_documents(
                texts, 
                self._embeddings, 
                path=self._db_path, 
                collection_name=self._collection_name,
                distance_func="Dot")
        '''

        if __debug__ :
            print(f"Loading file to vector db collection [{self._collection_name}]")

        return self

    def QA(self, question):
        """
        QA - semantic search
        :param self , question
        :return answer, source
        """

        chain_type_kwargs = {"prompt": self._prompt}

        if self._db is None :
            self._db = self.__init_vectordb__()
        if self._qa is None :
            if __debug__ :    
                print(">>> RetrievalQA.from_chain_type start..\n")
            self._qa = RetrievalQA.from_chain_type(
                                 llm=self._llm,
                                 chain_type="stuff",  # “stuff”, “map_reduce”, “refine”, “map_rerank”.
                                 retriever=self._db.as_retriever(),
                                 chain_type_kwargs=chain_type_kwargs,
                                 return_source_documents=True
                                 )
            if __debug__ :    
                print(">>> RetrievalQA.from_chain_type end..\n")
        if __debug__ :    
            print(">>> query start..\n")
        answer = self._qa({"query": question})
        if __debug__ : 
            print(">>> query end..\n")
        result = answer["result"].replace("\n","").replace("Answer:","")
        sources = answer['source_documents']
        
        if __debug__ :
            print("-"*150,"\n")
            print(f"Question: {question}")
            print(f"Answer: {result}")

        if __debug__ : 
            print("<<<>>> Result sources BEGIN..\n")
            ## print(f'{sources}')
            # dir(answer["sources"])
            print("<<<>>> Result END..\n")
        
        ### COMMENT OUT THE 4 LINES BELOW TO HIDE THE SOURCES
        if __debug__ :
            print(f"\nSources:")

        source_wrapped = []
        for idx, source in enumerate(sources):
            # dir(source)
            # wrapped = tr.fill(str(source.page_content), width=150)
            wrapped = str(source.page_content)

            if __debug__ :
                print(f"[{idx+1} : {source.metadata} ]: \n {wrapped}")
                print(f"{source}")
            #source_wrapped.append(f"[{idx+1} : {source.metadata} ] : \n {wrapped}")
            source_wrapped.append(f"[{idx+1}. source : {source.metadata['source']} ]: \n {wrapped}")
        if __debug__ :
            print("QA end..\n")
        #return result, str(sources)
        return result, '\n'.join(source_wrapped)
