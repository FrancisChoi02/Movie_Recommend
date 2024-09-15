import sqlite3
from dao.rating import get_rating_by_userId
from dao.movie import get_movie_with_movieId_dao
from dao.common import(
    split_genre_to_list,
    convert_genre_to_dict,
)
from service.movie_service import get_genre_score_from_movie,set_genre,get_genre_list_dict_from_movie


DATABASE_PATH = 'static/movie_recommend.sqlite'  # 替换为你的数据库路径

def create_users_table():
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # SQL 创建表语句
    query = '''
    CREATE TABLE IF NOT EXISTS users (
        userId INTEGER,
        username TEXT,
        passwd TEXT
    )
    '''

    # 执行创建表语句
    cursor.execute(query)

    # 提交事务
    conn.commit()

    # 关闭数据库连接
    conn.close()

def create_userRecommend_table():
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # SQL 创建表语句
    query = '''
    CREATE TABLE IF NOT EXISTS userRecommend (
        userId INTEGER,
        recommend TEXT,
        count INTEGER
    )
    '''

    # 执行创建表语句
    cursor.execute(query)

    # 提交事务
    conn.commit()

    # 关闭数据库连接
    conn.close()


def create_rating_table():
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # SQL 创建表语句
    query = '''
    CREATE TABLE IF NOT EXISTS rating (
        movieId INTEGER,
        rating REAL,
        timestamp INTEGER
    )
    '''

    # 执行创建表语句
    cursor.execute(query)

    # 提交事务
    conn.commit()

    # 关闭数据库连接
    conn.close()


def create_movie_table():
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # SQL 创建表语句
    query = '''
    CREATE TABLE IF NOT EXISTS movie (
        id INTEGER,
        name TEXT,
        url TEXT,
        time TEXT,
        genre TEXT,
        release_time TEXT,
        intro TEXT,
        directors TEXT,
        writers TEXT,
        starts TEXT,
    )
    '''

    # 执行创建表语句
    cursor.execute(query)

    # 提交事务
    conn.commit()

    # 关闭数据库连接
    conn.close()


def create_userGenre_table():
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # SQL 创建表语句
    query = '''
    CREATE TABLE IF NOT EXISTS userGenre (
        userId INTEGER,
        genre INTEGER,
        score REAL
    )
    '''

    # 执行创建表语句
    cursor.execute(query)

    # 提交事务
    conn.commit()

    # 关闭数据库连接
    conn.close()

# 创建表
def totol_create_all_table():
    create_users_table()
    create_rating_table
    create_userGenre_table()
    create_movie_table()
    create_userRecommend_table()


# 初始化用户偏好表
def create_user_genre_from_rating():
    for i in range(2,611):
        rating_result = get_rating_by_userId(str(i))

        temp_genre_array = []
        for rat in rating_result:
            genre_map=get_genre_list_dict_from_movie(rat[1],rat[2])
            temp_genre_array.append(genre_map)
          
        
        result = get_genre_score_from_movie(temp_genre_array)

        
        result_gerne=set_genre(rat[0],result)
        print(i)

if __name__ == '__main__':
    # 创建数据库
    totol_create_all_table()

    # 初始化用户偏好表
    create_user_genre_from_rating()