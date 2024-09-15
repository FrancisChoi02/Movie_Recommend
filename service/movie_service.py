import os
from service.openai import get_rag_information
from typing import List,Dict
from dao.movie import (
    get_movie_with_movieId_dao,
    get_recommend_movie_with_userId_dao,
    get_movie_with_genre_dao,
    get_movie_with_name_dao,
    get_movie_with_director_name_dao,
    get_movie_with_star_name_dao,
    get_rating_count_with_userId_dao,
)
from service.recommend.user_recommend import get_recommend_userId
from service.recommend.movie_recommend import get_user_recommend_movie_list
from dao.common import split_genre_to_list,convert_genre_to_dict
from dao.user import set_genre_dao
from entity.movie import Movie



COLLECTION_MOVIE = os.getenv("COLLECTION_MOVIE")

def get_genre_score_from_movie(genre_score_list):

    # 创建一个空列表来存储所有电影的类型评分
    all_genre_scores = []

    for result in  genre_score_list:
    # 对每部电影生成类型评分列表，并将它们添加到总列表中
        all_genre_scores.extend(result)


    # 创建一个空字典来存储每个类型的累积分数
    genre_totals = {}

    # 遍历所有类型评分，计算每个类型的总分
    for genre_score in all_genre_scores:
        genre = genre_score['genre']
        score = genre_score['score']
        if genre in genre_totals:
            genre_totals[genre] += score
        else:
            genre_totals[genre] = score

    # 将累积的分数转换回期望的列表格式
    # 除以 all_genre_scores 的总数
    total_entries = len(genre_score_list)
    
    final_list = [{'genre': genre, 'score': score / total_entries} for genre, score in genre_totals.items()]

    return final_list

# 获取一部电影的genre_list
def get_genre_list_from_movie(movieId,rate):
    temp_movie= get_movie_with_movieId_dao(movieId)
    movie_genre = temp_movie[0][-6]
    genre_list = split_genre_to_list(movie_genre)

    return genre_list


# 获取一部电影的genre_list_dict
def get_genre_list_dict_from_movie(movieId,rate):
    temp_movie= get_movie_with_movieId_dao(movieId)
    movie_genre = temp_movie[0][-6]
    genre_list = split_genre_to_list(movie_genre)
    genre_map = convert_genre_to_dict(genre_list,int(rate))


    return genre_map

# 根据genre字段获取对应的Id
def get_genreId(genre_str:str):
    genre_to_id = {
        "Musical": 1, "War": 2, "Crime": 3, "Romance": 4, "Fantasy": 5, "Drama": 6,
        "Music": 7, "Sci-Fi": 8, "Action": 9, "Comedy": 10, "Biography": 11,
        "Family": 12, "Horror": 13, "Short": 14, "Documentary": 15, "Film-Noir": 16,
        "Animation": 17, "Adventure": 18, "News": 19, "Mystery": 20, "Sport": 21,
        "History": 22, "Thriller": 23, "Western": 24
    } 

    # 如果genre_str不在字典中，返回0
    genreId = genre_to_id.get(genre_str, 0)

    return genreId

# 根据genre_id 获取对应 genre字段
def get_genreId_reverse(genre_id:str):
    genre_id_integer = int(genre_id)
    id_to_genre = {
        1: "Musical", 2: "War", 3: "Crime", 4: "Romance", 5: "Fantasy", 6: "Drama",
        7: "Music", 8: "Sci-Fi", 9: "Action", 10: "Comedy", 11: "Biography",
        12: "Family", 13: "Horror", 14: "Short", 15: "Documentary", 16: "Film-Noir",
        17: "Animation", 18: "Adventure", 19: "News", 20: "Mystery", 21: "Sport",
        22: "History", 23: "Thriller", 24: "Western"
    }
    
    genre_str = id_to_genre.get(genre_id_integer,"Musical")

    return genre_str

# 将偏好电影的类型设置为map
def set_genre(userId: str, genre_list: List[Dict]):
    # 定义genre到genreId的映射
    genre_to_id = {
        "Musical": 1, "War": 2, "Crime": 3, "Romance": 4, "Fantasy": 5, "Drama": 6,
        "Music": 7, "Sci-Fi": 8, "Action": 9, "Comedy": 10, "Biography": 11,
        "Family": 12, "Horror": 13, "Short": 14, "Documentary": 15, "Film-Noir": 16,
        "Animation": 17, "Adventure": 18, "News": 19, "Mystery": 20, "Sport": 21,
        "History": 22, "Thriller": 23, "Western": 24
    } 

    # 遍历genre_list并插入数据到userGen表
    for genre_map in genre_list:
        print(len(genre_list))
        
        genre_id = genre_to_id.get(genre_map["genre"])
        if genre_id:  # 确保genre有效
            rating = float(genre_map["score"])  # 将score从字符串转换为浮点数
            rating = round(rating, 3)  # 保留三位小数
            set_genre_dao(userId, genre_id, rating)
            
    return "设置成功"

# 根据movieId获取电影
def get_movie_by_movieId(movieId: str):
    temp_movie= get_movie_with_movieId_dao(movieId)
    
    if len(temp_movie)==0:
        return temp_movie
    else:
        movie_result = temp_movie[0]
        return movie_result


def extract_movie_name_from_map_string(data):
    # 将字符串数据转换为字典格式
    data_dict = eval(data)
    
    # 提取"name"字段的值
    name = data_dict.get('name', None)
    
    return name

def get_augmented_movie_name(movie_name:str):
    collection = COLLECTION_MOVIE
    _, result = get_rag_information(movie_name,collection)
    movie_name_augmented = extract_movie_name_from_map_string(result[0])
    
    return movie_name_augmented

# 电影名增强检索
def get_movie_with_search_name(movie_str):
    name = get_augmented_movie_name()
    movies = get_movie_with_name_dao(name)
    return movies

# 根据genre_id获取分类对应的电影列表
def get_movie_with_genre(genre_str:str):
    movie_list_raw = get_movie_with_genre_dao(genre_str)
    return movie_list_raw

# 获取director对应的作品
def get_movie_with_director_name(genre_str:str):
    movie_list_raw = get_movie_with_director_name_dao(genre_str)
    return movie_list_raw

# 获取star对应的作品
def get_movie_with_star_name(genre_str:str):
    movie_list_raw = get_movie_with_star_name_dao(genre_str)
    return movie_list_raw

# 根据userId获取推荐的电影列表
def get_recommend_movie_list_with_userId(userId:str):

    # 获取用户的评分电影数
    rating_count = get_rating_count_with_userId_dao(userId)
    # 如果评分电影小于5，则获取推荐用户的结果
    if rating_count < 5:
        similar_userId = get_recommend_userId(userId,5,10)
        movie_id_list=get_user_recommend_movie_list(similar_userId)
    else:
        movie_string= get_recommend_movie_with_userId_dao(userId)
        movie_id_list= split_genre_to_list(movie_string)
    return movie_id_list

def get_top_picks_movies():
    top_picks_id_list = ['318', '527', '2571', '2008', '79132']
    top_picks_list = []
    for id in top_picks_id_list:
            raw_tmp_movie = get_movie_by_movieId(id)
            print(raw_tmp_movie)
            tmp_movie = Movie(*raw_tmp_movie)
            top_picks_list.append(tmp_movie)
    return top_picks_list