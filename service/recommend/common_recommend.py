import sqlite3
import random

DATABASE_PATH = 'static/movie_recommend.sqlite'
def read_rating_data():
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)  # 替换为你的数据库文件路径
    cursor = conn.cursor()

    # 从rating表中读取数据
    data = []
    # cursor.execute('SELECT userId, genre, score FROM userGenre')
    cursor.execute('SELECT userId, movieId, rating FROM rating')
    for row in cursor.fetchall():
        data.append((int(row[0]), int(row[1]), float(row[2])))

    # 关闭数据库连接
    conn.close()

    return data

DATABASE_PATH = 'static/movie_recommend.sqlite'
def read_genre_data():
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)  # 替换为你的数据库文件路径
    cursor = conn.cursor()

    # 从userGenre表中读取数据
    data = []
    cursor.execute('SELECT userId, genre, score FROM userGenre')
    for row in cursor.fetchall():
        data.append((int(row[0]), int(row[1]), float(row[2])))

    # 关闭数据库连接
    conn.close()

    return data

def get_userItem_dict(data):
    pivot = 0.75
    test_dct = {}
    train_dct = {}
    # 按照1：3的比例划分测试集和训练集
    random.seed(random.randint(0, 10000))
    # 用户评分
    for user, item, rating in data:
        if random.random() >= pivot:
            test_dct.setdefault(user, dict())
            test_dct[user][item] = rating
        else:
            train_dct.setdefault(user, dict())
            train_dct[user][item] = rating
    userItem_dict = train_dct
    return userItem_dict