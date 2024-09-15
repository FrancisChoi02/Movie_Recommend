import sqlite3

DATABASE_PATH = 'static/movie_recommend.sqlite'

def get_rating_by_userId(userId: str):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # 检查用户是否存在
    cursor.execute(f"SELECT * FROM rating where userId = ?",(userId,)) 
    rating_info_raw = cursor.fetchall()
    
    # 关闭数据库连接
    conn.close()

    return rating_info_raw

# 获取用户对某个电影的评价记录
def get_rating_record(userId,movieId):
    # 假设DATABASE_PATH是你的数据库路径
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # 首先检查用户是否已经评价过这部电影
    cursor.execute("SELECT rating FROM rating WHERE userId = ? AND movieId = ?", (userId, movieId))
    result = cursor.fetchone()

    return result

# 返回用户评价的电影次数
def get_rating_record_times(userId):
    # 假设DATABASE_PATH是你的数据库路径
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT rating FROM ratings WHERE userId = ?", (userId,))
    results = cursor.fetchall()

    conn.close()

    return len(results)

def delete_rating_record(userId, movieId):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rating WHERE userId = ? AND movieId = ?", (userId, movieId))
    # 关闭数据库连接
    conn.close()

    return "Deleted"

def update_rating_record(userId,movieId,rate):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE rating SET rating = ? WHERE userId = ? AND movieId = ?", (rate, userId, movieId))
    # 关闭数据库连接
    conn.close()

    return "Updated"

def add_rating_record(userId,movieId,rate):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rating (userId, movieId, rating) VALUES (?, ?, ?)", (userId, movieId, rate))
    # 关闭数据库连接
    conn.close()

    return "Added"
