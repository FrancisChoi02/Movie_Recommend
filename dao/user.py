import sqlite3
from dao.common import get_db

# 假设你已经设置了数据库路径在环境变量中
DATABASE_PATH = 'static/movie_recommend.sqlite'

# 根据用户名获取用户信息
def get_user_by_name(username: str):

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # 检查用户是否存在
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_info_raw = cursor.fetchone()

    # 关闭数据库连接
    conn.close()

    return user_info_raw

# 根据用户名获取用户信息
def get_userId_by_name(username: str):

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # 检查用户是否存在
    cursor.execute("SELECT uid FROM users WHERE username = ?", (username,))
    user_info_raw = cursor.fetchone()

    # 关闭数据库连接
    conn.close()

    return user_info_raw

# 用户注册
def register_user_dao(username:str, password: str):

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    # 分配新的用户ID
    cursor.execute("SELECT MAX(userId) FROM users")
    max_id_result = cursor.fetchone()
    new_id = 611 if max_id_result[0] is None else max_id_result[0] + 1
    
    # genre先设为空值
    genre = ""
    cursor.execute("INSERT INTO users (userId, username, passwd) VALUES (?, ?, ?)", (new_id, username, password))

    conn.commit()  # 别忘了提交数据库事务

    return new_id

# 设置用户喜好标签
def set_genre_dao(user_id, genre_id, rating):
    conn = sqlite3.connect(DATABASE_PATH)
    # 执行SQL语句
    cursor = conn.cursor()
    cursor.execute("INSERT INTO userGenre (userId, genreId, rating) VALUES (?, ?, ?)", (user_id, genre_id, rating))
    conn.commit()  # 提交事务以保存更改
    conn.close()

# 设置用户喜好标签
def update_genre_dao(user_id, genre_id, rating):
    conn = sqlite3.connect(DATABASE_PATH)
    # 执行SQL语句
    cursor = conn.cursor()
    cursor.execute("INSERT INTO userGenre (userId, genreId, rating) VALUES (?, ?, ?)", (user_id, genre_id, rating))
    conn.commit()  # 提交事务以保存更改
    conn.close()

# 向userGenre表中更新数据
def upgrade_genre_with_count_dao(userId, genre_id, rate,count):
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # 首先获取当前的score和count值
    cursor.execute("SELECT score, count FROM userGenre WHERE userId = ? AND genre = ?", (userId, genre_id))
    result = cursor.fetchone()

    if result:
        # 获取
        current_score = result[-1]
        new_score = (current_score * count + rate) / (count + 1)
        #我想修改一下这里的逻辑，我想将原来的score赋值为：(score*count＋rate)/(count+1)
        cursor.execute("UPDATE userGenre SET score = ? WHERE userId = ? AND genre = ?", (new_score, userId, genre_id))
    else:
        cursor.execute("INSERT INTO userGenre (userId, genre, score, count) VALUES (?, ?, ?, 1)", (userId, genre_id, rate))
    conn.commit()
    conn.close()

# 往用户推荐结果表中添加数据
def set_user_recommend(userId,recommend_str,initial_count):
    conn = sqlite3.connect(DATABASE_PATH)
    # 执行SQL语句
    cursor = conn.cursor()
    cursor.execute("INSERT INTO userRecommend (userId, recommend, count) VALUES (?, ?, ?)", (userId, recommend_str, initial_count))
    conn.commit()  # 提交事务以保存更改
    conn.close()

