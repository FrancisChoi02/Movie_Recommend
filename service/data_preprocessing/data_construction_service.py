import re
import chromadb
import sqlite3
import os
import json
import asyncio
import pandas as pd
from chromadb import Collection
from typing import List,Tuple
from service.openai import(
    create_embedding_for_dataset_openai,
)
from entity.snowflake import(
    Snowflake
)


COLLECTION_MOVIE = os.getenv("COLLECTION_MOVIE")
COLLECTION_DIRECTOR = os.getenv("COLLECTION_DIRECTOR")
COLLECTION_STAR = os.getenv("COLLECTION_STAR")
COLLECTION_MIX = os.getenv("COLLECTION_MIX")


def get_metadata_array(source_meta):
    metadata_array = []
    for meta in source_meta:
        metadata = {'source_document':meta}
        metadata_array.append(metadata)
    return metadata_array

def get_document_map(question, answer):
    return {'name': question, 'movieId': answer}

def get_movie_map(name,director,star,genre):
    return {"movie_name":name, "directors":director, "star":star, "genre": genre}

async def add_data_to_collection(collection: Collection,key,value,metadata_array):
    embedded_array = await create_embedding_for_dataset_openai(key)
    
    # 初始化雪花算法实例
    snowflake = Snowflake(datacenter_id=1, worker_id=1)
    # 生成唯一的 IDs
    ids = [str(snowflake.get_id()) for _ in range(len(embedded_array))]

    final_metadata_array = get_metadata_array(metadata_array)

    # 构建复合document
    temp_array = []
    document_array = []
    temp_array = list(map(get_document_map, key, value))
    
    for temp in temp_array:
        document = str(temp)
        document_array.append(document)

    # 添加 “Question-Answer”
    collection.add(
        ids=ids,
        embeddings=embedded_array,
        documents=document_array,
        metadatas=final_metadata_array
    )
    # 添加 相关“Answer” 
    print("Adding data process finished")

async def add_data_to_collection_plain(collection: Collection,key,value,metadata_array):
    embedded_array = await create_embedding_for_dataset_openai(key)
    
    # 初始化雪花算法实例
    snowflake = Snowflake(datacenter_id=1, worker_id=1)
    # 生成唯一的 IDs
    ids = [str(snowflake.get_id()) for _ in range(len(embedded_array))]

    final_metadata_array = get_metadata_array(metadata_array)

    # 添加 “Question-Answer”
    collection.add(
        ids=ids,
        embeddings=embedded_array,
        documents=value,
        metadatas=final_metadata_array
    )

    # 添加 相关“Answer” 
    print("Adding data process finished")


async def build_movie_collection(movie_name_list,movie_id_list:List):
    metadata_array =  ['movie' for name in movie_name_list]
    collection_name = COLLECTION_MOVIE
    client = chromadb.HttpClient(host='localhost',port='1235')
    collection = client.get_or_create_collection(collection_name)

    await add_data_to_collection(collection,movie_name_list,movie_id_list,metadata_array)
    return


async def build_director_collection(director_list:List):
    metadata_array =  ['director' for name in director_list]
    
    collection_name = COLLECTION_DIRECTOR
    client = chromadb.HttpClient(host='localhost',port='1235')
    collection = client.get_or_create_collection(collection_name)

    await add_data_to_collection_plain(collection,director_list,director_list,metadata_array)
    return


async def build_star_collection(star_list: List):

    metadata_array =  ['star' for name in star_list]
    
    collection_name = COLLECTION_STAR
    client = chromadb.HttpClient(host='localhost',port='1235')
    collection = client.get_or_create_collection(collection_name)

    await add_data_to_collection_plain(collection,star_list,star_list,metadata_array)

    return

async def build_mix_collection(mix_dict:List):
    
    metadata_array =  ['mix' for mix in mix_dict]
    
    collection_name = COLLECTION_MIX
    client = chromadb.HttpClient(host='localhost',port='1235')
    collection = client.get_or_create_collection(collection_name)

    await add_data_to_collection_plain(collection,mix_dict,mix_dict,metadata_array)

    return

def dict_to_json_str(movie_info):
    # 将字典转换为JSON格式的字符串
    return json.dumps(movie_info)

def json_str_to_dict(json_str):
    # 将JSON格式的字符串转换回字典
    return json.loads(json_str)


def get_movie_names(mix_list):
    return list(set([movie['movie_name'] for movie in mix_list]))

def get_directors(mix_list):
    # Assuming directors can be a list, we'll flatten the list and remove duplicates
    return list(set([director for movie in mix_list for director in movie['directors']]))

def get_stars(mix_list):
    # Similarly, assuming stars can be a list and we want to flatten it
    return list(set([star for movie in mix_list for star in movie['stars']]))

def get_genres(mix_list):
    # Assuming a single movie can belong to multiple genres
    return list(set([genre for movie in mix_list for genre in movie['genre']]))

def get_movie_lists() -> Tuple[List[str], List[int]]:
    # 假设DATABASE_PATH是你的数据库路径
    DATABASE_PATH = 'static/movie_recommend.sqlite'

    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # 查询所有电影的ID和名称
    cursor.execute("SELECT id, name FROM movie")

    # 初始化两个空列表来存储电影ID和电影名
    movie_name_list = []
    movie_id_list = []

    # 遍历查询结果，填充列表
    for movie_id, movie_name in cursor.fetchall():
        movie_id_list.append(movie_id)
        movie_name_list.append(movie_name)

    # 关闭数据库连接
    conn.close()

    return movie_name_list, movie_id_list

def str_to_list(id_str:str):
    # 将字符串分割成字符串ID列表
    if id_str is not None:
        str_ids = id_str.split('|')
        # 将每个字符串ID转换为整数
        return [str_id for str_id in str_ids]
    else:
        return 

def get_director_star_list() -> Tuple[List[str], List[int]]:
    # 假设DATABASE_PATH是你的数据库路径
    DATABASE_PATH = 'static/movie_recommend.sqlite'

    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # 查询所有电影的ID和名称
    cursor.execute("SELECT directors, starts FROM movie")

    # 初始化两个空列表来存储电影ID和电影名
    movie_director_list = []
    movie_star_list = []

    # 遍历查询结果，填充列表
    for director, star in cursor.fetchall():
        temp_director_list = []
        temp_star_list = []
        if director is not None:
            temp_director_list = str_to_list(director)
            movie_director_list.extend(temp_director_list)
        if star is not None:
            temp_star_list = str_to_list(star)
            movie_star_list.extend(temp_star_list)    

    movie_director_list = list(set(movie_director_list))
    movie_star_list = list(set(movie_star_list))
    # 关闭数据库连接
    conn.close()

    return movie_director_list, movie_star_list

def get_mix_list() -> Tuple[List[str], List[int]]:
    # 假设DATABASE_PATH是你的数据库路径
    DATABASE_PATH = 'static/movie_recommend.sqlite'

    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # 查询所有电影的ID和名称
    cursor.execute("SELECT name, directors, starts, genre FROM movie")

    mix_list = []
    # 遍历查询结果，填充列表
    for name, directors, stars, genre in cursor.fetchall():
        movie_info = {
            "movie_name": name,
            "directors": directors,
            "stars": stars,
            "genre": genre
        }
        map_string= dict_to_json_str(movie_info)
        mix_list.append(map_string)

    # 关闭数据库连接
    conn.close()

    return mix_list


def rating_table_import():
    # Excel文件路径
    excel_file = 'static/ratings.csv'
    # SQLite数据库文件路径
    # sqlite_file = 'static/chatbot_data_for_demo.sqlite'
    sqlite_file = 'static/movie_recommend.sqlite'


    # 使用pandas读取Excel文件
    # df = pd.read_csv(excel_file, encoding='utf-8')
    df = pd.read_csv(excel_file, encoding='latin1')

    # 连接到SQLite数据库，如果文件不存在会自动创建
    conn = sqlite3.connect(sqlite_file)

    # 将DataFrame转换为SQL表，table_name是你希望在SQLite中创建的表名
    table_name = 'rating'
    df.to_sql(table_name, conn, if_exists='append', index=False)  # 假设我们不需要将DataFrame的索引作为数据存储

    # 关闭数据库连接
    conn.close()

    print("ENter")

def movie_table_import():
    # Excel文件路径
    excel_file = 'static/info.csv'
    # SQLite数据库文件路径
    # sqlite_file = 'static/chatbot_data_for_demo.sqlite'
    sqlite_file = 'static/movie_recommend.sqlite'


    # 使用pandas读取Excel文件
    # df = pd.read_csv(excel_file, encoding='utf-8')
    df = pd.read_csv(excel_file, encoding='latin1')

    # 连接到SQLite数据库，如果文件不存在会自动创建
    conn = sqlite3.connect(sqlite_file)

    # 将DataFrame转换为SQL表，table_name是你希望在SQLite中创建的表名
    table_name = 'table'
    df.to_sql(table_name, conn, if_exists='append', index=False)  # 假设我们不需要将DataFrame的索引作为数据存储

    # 关闭数据库连接
    conn.close()

    print("ENter")


async def total_collection_construcion():
    movie_name_list, movie_id_list = get_movie_lists()
    movie_name_list = movie_name_list
    movie_id_list = movie_id_list

    director_list,start_list=get_director_star_list()
    director_list = director_list
    start_list = start_list

    mix_list = get_mix_list()
    mix_list = mix_list

    await build_movie_collection(movie_name_list,movie_id_list)
    await build_director_collection(director_list)
    await build_star_collection(start_list)
    await build_mix_collection(mix_list)

if __name__ == '__main__':
    movie_table_import()
    rating_table_import
    asyncio.run(total_collection_construcion())