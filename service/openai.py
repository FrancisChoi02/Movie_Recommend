import os
import chromadb
import re
from dotenv import load_dotenv
from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import AzureOpenAIEmbeddings
from entity.aoai import AoaiResponse
import requests
import json


load_dotenv()
CHROMA_PORT = os.getenv('CHROMA_PORT')
COLLECTION_MIX = os.getenv("COLLECTION_MIX")

OPENAI_API_BASE_VISION = os.getenv('OPENAI_API_BASE_VISION')
DEPLOYMENT_GPT4 = os.getenv('DEPLOYMENT_GPT4')
OPENAI_API_VERSION = os.getenv('OPENAI_API_VERSION')
OPENAI_API_KEY_VISION = os.getenv('OPENAI_API_KEY_VISION')


def get_query_openai_embedding(question:str):
    ai_ebd = get_azureOpenAIEmbeddings()
    ai_embedding_result = ai_ebd.embed_query(question)
    return ai_embedding_result

def get_azureOpenAIEmbeddings():
    model_deployment = os.getenv("DEPLOYMENT_EBD")
    api_url = os.getenv("OPENAI_API_BASE")
    key = os.getenv("OPENAI_API_KEY")
    openAI_api_type = os.getenv("OPENAI_API_TYPE")

    return AzureOpenAIEmbeddings(deployment=model_deployment,openai_api_base=api_url,openai_api_key=key,openai_api_type=openAI_api_type)

async def create_embedding_for_dataset_openai(question_set):
    model_deployment = os.getenv("DEPLOYMENT_EBD")
    api_url = os.getenv("OPENAI_API_BASE")
    key = os.getenv("OPENAI_API_KEY")
    
    ai_embeddings =get_azureOpenAIEmbeddings()
    embedding_array= await ai_embeddings.aembed_documents(question_set)
    return embedding_array


async def create_embedding_openai_embedding(question):
    model_deployment = os.getenv("DEPLOYMENT_EBD")
    api_url = os.getenv("OPENAI_API_BASE")
    key = os.getenv("OPENAI_API_KEY")
    openAI_api_type = os.getenv("OPENAI_API_TYPE")

    ai_embeddings = AzureOpenAIEmbeddings(deployment=model_deployment,openai_api_base=api_url,openai_api_key=key,openai_api_type=openAI_api_type)
    ai_embedding_result = ai_embeddings.embed_query(question)
    return ai_embedding_result


async def get_aoai_gpt_response(question: str,prompt:str):
    headers = {
        'Content-Type': 'application/json',
        'api-key': OPENAI_API_KEY_VISION
    }
    
    reqPayload = {
        "messages": [
            {
                'role': 'system',
                'content': prompt
            },
            {
                'role': 'user',
                'content': question
            }
        ],
        "temperature": 0,
        "top_p": 0.95,
    }
    response = requests.post(
        f'{OPENAI_API_BASE_VISION}openai/deployments/{DEPLOYMENT_GPT4}/chat/completions?api-version={OPENAI_API_VERSION}',
        json=reqPayload,
        headers=headers,
        timeout=120
    )
    return response

async def call_gpt(query_string, prompt):
    aoai_response = await get_aoai_gpt_response(query_string, prompt)
    resp = aoai_response.json()
    result_aoai = AoaiResponse(resp)
    text_content = result_aoai.reply

    return text_content

# 从数据库中获取满足相似度要求的数据
def get_rag_information(original_enqury: str,collection:str):
    matched = False
    answer_array = []

    client = chromadb.HttpClient(host='localhost',port=CHROMA_PORT)
    collection_name = collection
    ai_ebd = get_azureOpenAIEmbeddings()

    vectorstore = Chroma(
        collection_name= collection_name,
        client=client,
        embedding_function=ai_ebd
        )
    embedding = get_query_openai_embedding(original_enqury)
    result = vectorstore.similarity_search_by_vector_with_relevance_scores(embedding=embedding)

    
    print(collection)
    # 查看Q-A类信息
    for res in result:
        print(res[1])
        print(res[0].page_content)

        if res[1]< 0.1:
            answer_array.append(res[0].page_content)
            break
        elif res[1] < 0.15:
            answer_array.append(res[0].page_content)
            break
        elif res[1] < 0.21:
            answer_array.append(res[0].page_content)
            break
        elif res[1] < 0.35:
            answer_array.append(res[0].page_content)
            break
        elif res[1] < 0.4:
            answer_array.append(res[0].page_content)
            break
    print(answer_array)


    if len(answer_array) > 0:
        matched = True

    return matched,answer_array



# 从数据库中获取满足相似度要求的数据
async def get_generative_recommend(search_str: str):

    with open('static/prompt/tag_extraction.txt','r') as f_2:
        tag_extraction_prompt = f_2.read()
    
    data_summary = await call_gpt(search_str,tag_extraction_prompt)

    client = chromadb.HttpClient(host='localhost',port=CHROMA_PORT)
    collection_name = COLLECTION_MIX
    ai_ebd = get_azureOpenAIEmbeddings()

    vectorstore = Chroma(
        collection_name= collection_name,
        client=client,
        embedding_function=ai_ebd
        )
    embedding = get_query_openai_embedding(data_summary)
    result = vectorstore.similarity_search_by_vector_with_relevance_scores(embedding=embedding)

    movie_recommend_list = []
 
    for res in result:
        print(res[1])
        print(res[0].page_content)

        if res[1] < 0.45:
            movie_recommend_list.append(res[0].page_content)

    return movie_recommend_list


