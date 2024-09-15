# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3



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
table_name = 'movie'
df.to_sql(table_name, conn, if_exists='append', index=False)  # 假设我们不需要将DataFrame的索引作为数据存储

# 关闭数据库连接
conn.close()

print("ENter")