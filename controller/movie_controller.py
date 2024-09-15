import sqlite3
import json
from service.login_service import get_user_name
from service.register_service import register_user,set_genre
from fastapi import APIRouter, Path,Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from entity.movie import Movie
from typing import List
from service.movie_service import (
    get_movie_by_movieId,
    get_genreId_reverse,
    get_movie_with_genre,
    get_recommend_movie_list_with_userId,
    get_top_picks_movies,
    get_movie_with_search_name,
)
from service.recommend.movie_recommend import recommend_similar_movies,get_generative_recommend
from service.openai import call_gpt

movie_recommend_router = APIRouter()
movie_genre_router = APIRouter()
movie_router = APIRouter()
movie_search_router = APIRouter()


@movie_search_router.post("/movie_search")
async def movie_search_controller(search_str: str = Form(...)):
    
    with open('static/prompt/recommend_detection.txt','r') as f_1:
        flag_prompt = f_1.read()

    flag = await call_gpt(search_str,flag_prompt)
    movie_list = []
    if flag == 'Yes':
        movie_list = get_movie_with_search_name(search_str)

    else:
        movie_list= await get_generative_recommend(search_str)
    if len(movie_list) == 0:
        return json.dumps({"movie_search_result": "There is no result"})
    else:
        response_data = {
        "movie_search_result": [movie.to_dict() for movie in movie_list]
    }
        return response_data


@movie_router.get("/movie/{movie_id}")
async def movie_controller(movie_id: str = Path(...)):
    raw_movie=get_movie_by_movieId(movie_id)
    
    if len(raw_movie) < 0:
        return "There is no relevant movie information"
    else:
        movie = Movie(*raw_movie)
        movie_id_integer = int(movie_id)

        similar_movie_result = []
        similar_movie_list = recommend_similar_movies(movie_id_integer)
        if len(similar_movie_list)>0:
            similar_movie_id_list = [item[0] for item in similar_movie_list]

            for id in similar_movie_id_list:
                raw_tmp_movie = get_movie_by_movieId(id)
                tmp_movie = Movie(*raw_tmp_movie)
                similar_movie_result.append(tmp_movie)

    # 构建JSON格式的响应
    response_data = {
        "movie": movie.to_dict(),
        "similar_movies": [similar_movie.to_dict() for similar_movie in similar_movie_result]
    }

    # 将JSON格式的响应返回给前端
    return json.dumps(response_data)


# 根据genre_id 获取具体分类的电影
@movie_genre_router.get("/movie_genre/{genre_id}")
async def movie_genre_controller(genre_id: str = Path(...)):
    
    # 根据genre_id 获取对应的genre_str字段
    genre_id_integer = int(genre_id)
    genre_str = get_genreId_reverse(genre_id_integer)
    # 根据 genre_str  获取movieList
    movie_list_raw = get_movie_with_genre(genre_str)

    movie_list = []
    if len(movie_list_raw) > 0:
        for movie in movie_list_raw:
            tmp_movie = Movie(*movie)
            movie_list.append(tmp_movie)

    print(len(movie_list))

    response_data = {
        "genre_movie": [movie.to_dict() for movie in movie_list]
    }
    
    return json.dumps(response_data)


# 基于用户标签的推荐算法
movie_recommend_router = APIRouter()
@movie_recommend_router.get("/movie_recommend/{user_id}")
async def movie_recommend_for_user(user_id:str = Path(...)):

    # 获取Top Pick
    top_picks_movies = get_top_picks_movies()
    # 获取User_recommend_list
    recommend_movie_list = []
    movie_id_list = get_recommend_movie_list_with_userId(user_id)
    if len(movie_id_list) > 0:
        for id in movie_id_list:
            raw_tmp_movie = get_movie_by_movieId(id)
            tmp_movie = Movie(*raw_tmp_movie)
            recommend_movie_list.append(tmp_movie)

    # 构建JSON格式的响应
    response_data = {
        "movie": [movie.to_dict() for movie in top_picks_movies],
        "similar_movies": [recommend_movie.to_dict() for recommend_movie in recommend_movie_list]
    }

    # 将JSON格式的响应返回给前端
    return json.dumps(response_data) 

        
    

