import sqlite3
import random
import os
from service.recommend.movie_recommend import get_item_similarity_matrix,get_user_recommend_movie_list
from service.movie_service import get_movie_by_movieId
from service.recommend.user_recommend import get_recommend_userId
from service.register_service import create_register_genre_list
from service.openai import get_rag_information
from entity.movie import Movie
from typing import List,Dict


def split_genre_to_list(genre_str:str):
    # 原始字符串
    
    # 使用 split() 方法按 '|' 分割字符串，并将结果存储在列表中
    list_of_genres = genre_str.split('|')

    return list_of_genres


def convert_genre_to_dict(list_of_genres, rating: int):
    #组成一个List[Dict],如 "[{"genre":,"Adventure","score": 2},{"genre":,"Comedy","score": 2}]"
    list_of_genre_scores = []

    for genre in list_of_genres:
        # 创建一个包含当前类型和评分的字典
        genre_score = {"genre": genre, "score": rating}
        # 将这个字典添加到列表中
        list_of_genre_scores.append(genre_score)
    return list_of_genre_scores 

# 将偏好电影的类型设置为map
def set_genre(username: str, genre_list: List[Dict]):
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
        genre_id = genre_to_id.get(genre_map["genre"])
        if genre_id:  # 确保genre有效
            rating = int(genre_map["score"])  # 假设score是字符串类型，需要转换为整数
            print(username, genre_id, rating)
            print(username)
            
    return "设置成功"

# 将用户所有的评分记录,平均成对应的评分矩阵
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
    print(total_entries)
    final_list = [{'genre': genre, 'score': score / total_entries} for genre, score in genre_totals.items()]

    print(final_list)
    return final_list




DATABASE_PATH = 'static/movie_recommend.sqlite'
def get_top_picks_movies():
    top_picks_id_list = ['318', '527', '2571', '2008', '79132']
    top_picks_list = []
    for id in top_picks_id_list:
            raw_tmp_movie = get_movie_by_movieId(id)
            print(raw_tmp_movie)
            tmp_movie = Movie(*raw_tmp_movie)
            top_picks_list.append(tmp_movie)
    return top_picks_list



# userId = "22"
# k = 20
# count = 10
# recommend = get_user_recommend_movie_list(userId,k,count)
# print(recommend)



movie_list = get_top_picks_movies()
print(movie_list)


# # 使用字典推导式将两个列表合并成一个字典
# ratings_dict = {movie_id: score for movie_id, score in zip(id_list, score_list)}

# user_raw = get_recommend_userId(ratings_dict,10,5)

# print(user_raw)




# # 测试函数
# genre_str = "Adventure|Animation|Children|Comedy|Fantasy"
# genre_list = split_genre_to_list(genre_str)
# rating = 2
# print(genre_list)

# result = convert_genre_to_dict(genre_list , rating)
# print(result)


