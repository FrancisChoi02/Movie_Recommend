import csv
import random
import pickle
from tools import timer
from math import sqrt, log
import sqlite3
import time

DATABASE_PATH = 'static/movie_recommend.sqlite'

class Recommend_Solution():
    def __init__(self, k, count):
        # 读入的原始数据集
        self.data = []

        self.test_dct = {}
        self.train_dct = {}
        # 推荐物品的字典，格式是 { item:value, ... }
        # self.recommend_dct = dict()
        # 最后的推荐列表，是按照兴趣值从大到小排序过后的列表,格式为[(item,value),(item,value)...]
        # self.recommend_lst = []
        # 用于记录用户之间的相似度，格式为 { user1:{ user2:value, user3:value...}, ... }
        self.item_similarity_matrix = dict()

        # 相似用户数量
        self.k = k
        # 10个推荐物品
        self.count = count

        # 记录每个用户评分的物体 { 1:{2,4,6...} , ... }
        self.user_item_dct = dict()
        # 记录每个物体评过分的用户 { 1:{1,2,4...} , ... }
        self.item_user_dct = dict()

    @timer
    def readData(self):
        # 连接到SQLite数据库
        conn = sqlite3.connect(DATABASE_PATH)  # 替换为你的数据库文件路径
        cursor = conn.cursor()

        # 从rating表中读取数据
        cursor.execute('SELECT userId, movieId, rating FROM rating')
        # cursor.execute('SELECT userId, genre, score FROM userGenre')

        # 获取50条数据
        for row in cursor.fetchmany(1000):
        # for row in cursor.fetchall():
            self.data.append((int(row[0]), int(row[1]), float(row[2])))

        # 关闭数据库连接
        conn.close()
                    
    @timer
    def splitData(self, pivot=0.75):
        # 按照1：3的比例划分测试集和训练集
        random.seed(random.randint(0, 10000))
        # 用户评分
        for user, item, rating in self.data:
            if random.random() >= pivot:
                self.test_dct.setdefault(user, dict())
                self.test_dct[user][item] = rating
            else:
                self.train_dct.setdefault(user, dict())
                self.train_dct[user][item] = rating
        # 节省空间
        del self.data


    @timer
    def builtDict(self):
        # 此函数用于建立起user_item_dct和item_user_dct
        # 两个dct格式类似于 { user1:{ a,s,d...} ,user2:{q,w,e...}, ...}
        # { Item1:{u1,u2..}, Item2:{u3,u6...} }

        # 用户物品倒排表就是训练集
        self.user_item_dct = self.train_dct

        for user, item_dct in self.user_item_dct.items():
            # u 用户，i 物品
            for item in item_dct.keys():
                self.item_user_dct.setdefault(item, set())
                self.item_user_dct[item].add(user)
  

    @timer
    def ItemCF_Norm(self):
        # 生成物品相似矩阵,使用字典存储，格式为 { user:{ user1: 相似度1, user2:相似度2}... ,}
        # 步骤：
        # 1.两两计算物品之间的相似度Wij
        # 2.Wij的计算方法是，喜欢i物品的用户和喜欢j物品的用户交集/根号下喜欢i物品的用户个数*喜欢j物品的用户个数

        for item1, users1 in self.item_user_dct.items():
            self.item_similarity_matrix.setdefault(item1, dict())
            for item2, users2 in self.item_user_dct.items():
                if item1 == item2:
                    continue
                if len(self.item_user_dct[item1]) == 0 or len(self.item_user_dct[item2]) == 0:
                    self.item_similarity_matrix[item1][item2] = 0
                    continue

                self.item_similarity_matrix[item1][item2] = len(
                    self.item_user_dct[item1] & self.item_user_dct[item2]) / sqrt(
                    len(self.item_user_dct[item1]) * len(self.item_user_dct[item2]))

        # ItemCF-Norm额外的一步，对相似矩阵做归一化
        for item1, items in self.item_similarity_matrix.items():
            # 取到相似度最大的值
            ms = max(items)
            for item2 in items:
                if item2 != 0:
                    # 归一化
                    item2 /= ms

        # 将item_similarity_matrix保存到文件
        with open('static/item_similarity_matrix.pkl', 'wb') as f:
            pickle.dump(self.item_similarity_matrix, f)


class Genre_Solution():
    def __init__(self, k, count):
        # 读入的原始数据集
        self.data = []

        self.test_dct = {}
        self.train_dct = {}
        # 推荐物品的字典，格式是 { item:value, ... }
        # self.recommend_dct = dict()
        # 最后的推荐列表，是按照兴趣值从大到小排序过后的列表,格式为[(item,value),(item,value)...]
        # self.recommend_lst = []
        # 用于记录用户之间的相似度，格式为 { user1:{ user2:value, user3:value...}, ... }
        self.item_similarity_matrix = dict()

        # 相似用户数量
        self.k = k
        # 10个推荐物品
        self.count = count

        # 记录每个用户评分的物体 { 1:{2,4,6...} , ... }
        self.user_item_dct = dict()
        # 记录每个物体评过分的用户 { 1:{1,2,4...} , ... }
        self.item_user_dct = dict()

    @timer
    def readData(self):
        # 连接到SQLite数据库
        conn = sqlite3.connect(DATABASE_PATH)  # 替换为你的数据库文件路径
        cursor = conn.cursor()

        # 从rating表中读取数据

        cursor.execute('SELECT userId, genre, score FROM userGenre')

        # 获取50条数据
        for row in cursor.fetchmany(1000):
        # for row in cursor.fetchall():
            self.data.append((int(row[0]), int(row[1]), float(row[2])))

        # 关闭数据库连接
        conn.close()
                    
    @timer
    def splitData(self, pivot=0.75):
        # 按照1：3的比例划分测试集和训练集
        random.seed(random.randint(0, 10000))
        # 用户评分
        for user, item, rating in self.data:
            if random.random() >= pivot:
                self.test_dct.setdefault(user, dict())
                self.test_dct[user][item] = rating
            else:
                self.train_dct.setdefault(user, dict())
                self.train_dct[user][item] = rating
        # 节省空间
        del self.data


    @timer
    def builtDict(self):
        # 此函数用于建立起user_item_dct和item_user_dct
        # 两个dct格式类似于 { user1:{ a,s,d...} ,user2:{q,w,e...}, ...}
        # { Item1:{u1,u2..}, Item2:{u3,u6...} }

        # 用户物品倒排表就是训练集
        self.user_item_dct = self.train_dct

        for user, item_dct in self.user_item_dct.items():
            # u 用户，i 物品
            for item in item_dct.keys():
                self.item_user_dct.setdefault(item, set())
                self.item_user_dct[item].add(user)
  

    @timer
    def ItemCF_Norm(self):
        # 生成物品相似矩阵,使用字典存储，格式为 { user:{ user1: 相似度1, user2:相似度2}... ,}
        # 步骤：
        # 1.两两计算物品之间的相似度Wij
        # 2.Wij的计算方法是，喜欢i物品的用户和喜欢j物品的用户交集/根号下喜欢i物品的用户个数*喜欢j物品的用户个数

        for item1, users1 in self.item_user_dct.items():
            self.item_similarity_matrix.setdefault(item1, dict())
            for item2, users2 in self.item_user_dct.items():
                if item1 == item2:
                    continue
                if len(self.item_user_dct[item1]) == 0 or len(self.item_user_dct[item2]) == 0:
                    self.item_similarity_matrix[item1][item2] = 0
                    continue

                self.item_similarity_matrix[item1][item2] = len(
                    self.item_user_dct[item1] & self.item_user_dct[item2]) / sqrt(
                    len(self.item_user_dct[item1]) * len(self.item_user_dct[item2]))

        # ItemCF-Norm额外的一步，对相似矩阵做归一化
        for item1, items in self.item_similarity_matrix.items():
            # 取到相似度最大的值
            ms = max(items)
            for item2 in items:
                if item2 != 0:
                    # 归一化
                    item2 /= ms

        # 将item_similarity_matrix保存到文件
        with open('user_genre_similarity_matrix.pkl', 'wb') as f:
            pickle.dump(self.item_similarity_matrix, f)



@timer
def execute_model_recommend(k, count, times=3):

    for i in range(times):
        print('-' * 30)
        s = Recommend_Solution(k, count)
        s.readData()
        s.splitData()
        s.builtDict()
        s.ItemCF_Norm()

@timer
def execute_model_genre(k, count, times=3):

    for i in range(times):
        print('-' * 30)
        s = Genre_Solution(k, count)
        s.readData()
        s.splitData()
        s.builtDict()
        s.ItemCF_Norm()


def refresh_rating_matrix():
    while True:
        execute_model_recommend(10, 5, 1)
        print("Finish refreshing rating matrix")
        time.sleep(600)  # 10分钟 = 600秒

def refresh_userGenre_matrix():
    while True:
        execute_model_genre(10, 5, 1)
        print("Finish refreshing userGenre matrix")
        time.sleep(600)  # 10分钟 = 600秒


    

 
