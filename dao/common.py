import sqlite3
import os
import time

# 假设你已经设置了数据库路径在环境变量中
DATABASE_PATH = 'static/movie_recommend.sqlite'



# 使用依赖项获取数据库连接
def get_db():
    # 连接到SQLite数据库，如果文件不存在会自动创建
    conn = sqlite3.connect(DATABASE_PATH)
    return 


# 获取当前UNIX时间戳
def get_timestamp():
    current_timestamp = int(time.time())
    return 
    

# 直接执行SQL
def get_data_with_sql(sql_query: str):
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # 执行查询
    cursor.execute(sql_query)

    # 获取所有匹配的记录
    datas = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    return datas


def split_genre_to_list(genre_str:str):
    # 原始字符串
    
    # 使用 split() 方法按 '|' 分割字符串，并将结果存储在列表中
    if genre_str is not None:
        list_of_genres = genre_str.split('|')
    else:
        list_of_genres = ['Adventure']

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