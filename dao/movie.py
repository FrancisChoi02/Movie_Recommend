import sqlite3
from typing import List,Dict

DATABASE_PATH = 'static/movie_recommend.sqlite'

def get_moive_dao(movieId:str):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # 检查用户是否存在
    cursor.execute("SELECT * FROM movie WHERE id = ?", (movieId))
    user_info_raw = cursor.fetchone()

    # 关闭数据库连接
    conn.close()

    return user_info_raw

# 查找某个固定类别的电影
def get_movie_with_genre_dao(genre_str: str):
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    query = f"SELECT * FROM movie WHERE genre LIKE '%{genre_str}%'"

    # 执行查询
    cursor.execute(query)

    # 获取所有匹配的记录
    movies = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    return movies

# 查找某个固定类别的电影
def get_movie_with_name_dao(movie_str: str):
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    query = f"SELECT * FROM movie WHERE name LIKE '%{movie_str}%'"

    # 执行查询
    cursor.execute(query)

    # 获取所有匹配的记录
    movies = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    return movies


def get_rating_count_with_userId_dao(userId: str):
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    query = f"SELECT COUNT(*) FROM rating WHERE userId LIKE '%{userId}%'"

    # 执行查询
    cursor.execute(query)

    # 获取所有匹配的记录
    rating_count = cursor.fetchone()[0]

    # 关闭数据库连接
    conn.close()

    return rating_count

def get_movie_with_director_name_dao(director_str: str):
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    query = f"SELECT * FROM movie WHERE directors LIKE '%{director_str}%'"

    # 执行查询
    cursor.execute(query)

    # 获取所有匹配的记录
    movies = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    return movies

def get_movie_with_star_name_dao(star_str: str):
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    query = f"SELECT * FROM movie WHERE stars LIKE '%{star_str}%'"

    # 执行查询
    cursor.execute(query)

    # 获取所有匹配的记录
    movies = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    return movies

# 通过字符串Id查找某个固定类别的电影
def get_movie_with_movieId_dao(movieId: str):
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    query = f"SELECT * FROM movie WHERE id = ?"

    # 执行查询
    cursor.execute(query,(movieId,))

    # 获取所有匹配的记录
    movies = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    return movies

def get_recommend_movie_with_userId_dao(userId:str):
        # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    query = f"SELECT * FROM userRecommend WHERE id = ?"

    # 执行查询
    cursor.execute(query,(userId,))

    # 获取所有匹配的记录
    movie_list_string = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    return movie_list_string

def get_recommend_movie_with_userId_dao(userId:str):
        # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    query = f"SELECT * FROM userRecommend WHERE id = ?"

    # 执行查询
    cursor.execute(query,(userId,))

    # 获取所有匹配的记录
    movie_list_string = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    return movie_list_string

# {"movie":"Toy Story", "director":"John Lasseter", "writer":"NULL","start":"Kevin Bacon"}

# 通过movieId获取电影封面URL
def get_movie_posterURL_with_movieId_dao(movieId: str):
    poster_URL = f'D:\\Movie_Recommend\\static\\poster\\{movieId}.jpg'
    return poster_URL

# # 向userGenre表中插入新数据
# def set_genre_dao(userId, genre_id, rating):
#     # 连接到SQLite数据库
#     conn = sqlite3.connect(DATABASE_PATH)
#     cursor = conn.cursor()

#     query = 'INSERT INTO userGenre (userId, genre, score) VALUES (?, ?, ?)'

#     cursor.execute(query, (userId, genre_id, rating))
#     conn.commit()
#     conn.close()




