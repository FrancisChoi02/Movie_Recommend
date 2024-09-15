import pickle
import json
from service.openai import call_gpt
from service.recommend.common_recommend import(
    read_rating_data,
    read_genre_data,
    get_userItem_dict,
)
from service.movie_service import(
    get_movie_with_genre,
    get_movie_with_search_name,
    get_movie_with_director_name,
    get_movie_with_star_name,
)

def count_empty_dict_members(json_str):
    # 将JSON格式字符串转换为字典
    data = json.loads(json_str)
    
    # 初始化空值成员数量
    empty_count = 0
    
    # 遍历字典，检查空值成员数量
    for key, value in data.items():
        if value == "":
            empty_count += 1
    
    return empty_count


def process_empty_dict_members(json_str, empty_count):
    # 将JSON格式字符串转换为字典
    data = json.loads(json_str)
    
    # 根据空值成员数量和具体空值成员情况执行处理流程
    if empty_count == 3 and data.get('movie_name', "") == "":
        # 进入movie_name对应的处理流程
        movie_info = {
            "movie_name": "Unknown",
            "directors": data.get('directors', ""),
            "stars": data.get('stars', ""),
            "genre": data.get('genre', "")
        }
        map_string = json.dumps(movie_info)
        
        print("处理movie_name为空的情况：")
        print(map_string)
    # 可根据需要添加其他条件和处理流程
    else:
        print("未满足条件的处理流程")

# 基于生成式模型的推荐算法
async def get_generative_recommend(search_str: str):
    with open('static/prompt/recommend_detection.txt', 'rb') as f:
        prompt = f.read()

    # 获取电影描述的数据摘要
    data_summarization = await call_gpt(search_str,prompt)

    # 统计电影摘要的成员缺失情况
    empty_member = count_empty_dict_members(data_summarization)

    result_list = []

    # 根据对应的电影摘要数量获取电影信息
    if empty_member == 3:
        if data_summarization.get('movie_name', "") != "":
            name_information = data_summarization.get('movie_name', "") 
            result_list = get_movie_with_search_name(name_information)
            return
        elif data_summarization.get('directors', "") != "":
            director_information = data_summarization.get('directors', "") 
            result_list = get_movie_with_director_name(director_information)
        elif data_summarization.get('', "") != "":
            star_information = data_summarization.get('stars', "") 
            result_list = get_movie_with_star_name(star_information)
        elif data_summarization.get('genre', "") != "":
            genre_infomation = data_summarization.get('genre', "") 
            result_list = get_movie_with_genre(genre_infomation)
    else: # 根据数据摘要获取推荐电影
        result_list = get_generative_recommend(search_str)
        


    return result_list


def get_item_similarity_matrix():
    with open('D:\\Movie_Recommend\\static\\item_similarity_matrix.pkl', 'rb') as f:
        item_similarity_matrix = pickle.load(f)
    return item_similarity_matrix


# 根据movieId推荐相似电影
def recommend_similar_movies(target_movie:int, N=5):
    item_similarity_matrix = get_item_similarity_matrix()

    # 检查目标电影是否在相似度矩阵中
    if target_movie not in item_similarity_matrix:
        print("empty")
        return []
        
    # 获取与目标电影相似的电影及其相似度分数
    similar_movies = item_similarity_matrix[target_movie].items()

    # 根据相似度对电影进行排序，取前N部电影
    recommended_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[:N]

    # 返回推荐电影的列表
    return recommended_movies
    

# 根据userId直接返回推荐列表
def recommend_user_Item(user:int,user_item_dct,item_similarity_matrix,k,count):
    # 每次找k部相似的电影，最后推荐count部
    rank = dict()
    watched_movies = user_item_dct[user]
    
    for movie, rating in watched_movies.items():
        if movie not in item_similarity_matrix:
            continue  # 如果不在，则跳过此次循环
        # 相似电影和权重
        for related_movie, w in sorted(item_similarity_matrix[movie].items(), key=lambda x: x[1],
                                        reverse=True)[:k]:
            if related_movie in watched_movies.keys():
                continue
            rank.setdefault(related_movie, 0)
            rank[related_movie] += w * float(rating)
    return sorted(rank.items(), key=lambda x: x[1], reverse=True)[:count]


# 根据UserId获取用户推荐电影列表
def get_user_recommend_movie_list(userId_str:str,k,count):
    userId = int(userId_str)
    rating_result = read_rating_data()
    matrix = get_item_similarity_matrix()
    
    # 获取用户评价的电影，根据用户评价电影进行相似推荐
    userItem_dict = get_userItem_dict(rating_result)

    recommend_list = recommend_user_Item(userId,userItem_dict,matrix,k,count)

    return recommend_list

