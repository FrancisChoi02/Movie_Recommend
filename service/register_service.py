from typing import List,Dict
from dao.user import register_user_dao,set_genre_dao,get_userId_by_name,set_genre_dao


def register_user(username,password):
    new_userId = register_user_dao(username,password)

    return new_userId


def set_genre_by_userId(user_id: str, genre_list: List[Dict]):
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
            set_genre_dao(user_id, genre_id, rating)
            print(user_id)
            
    return True



    
# 设置用户喜好表
def set_genre(username: str, genre_list: List[Dict]):
    # 定义genre到genreId的映射
    genre_to_id = {
        "Musical": 1, "War": 2, "Crime": 3, "Romance": 4, "Fantasy": 5, "Drama": 6,
        "Music": 7, "Sci-Fi": 8, "Action": 9, "Comedy": 10, "Biography": 11,
        "Family": 12, "Horror": 13, "Short": 14, "Documentary": 15, "Film-Noir": 16,
        "Animation": 17, "Adventure": 18, "News": 19, "Mystery": 20, "Sport": 21,
        "History": 22, "Thriller": 23, "Western": 24
    } 
    
    user_info_raw = get_userId_by_name(username)
    if user_info_raw :
        user_id = user_info_raw [0]
    else:
        # 用户名不存在
        return "用户不存在"

    # 遍历genre_list并插入数据到userGen表
    for genre_map in genre_list:
        genre_id = genre_to_id.get(genre_map["genre"])
        if genre_id:  # 确保genre有效
            rating = int(genre_map["score"])  # 假设score是字符串类型，需要转换为整数
            set_genre_dao(user_id, genre_id, rating)
            print(user_id)
            
    return "设置成功"

# 获取用于 查找相似用户 的genre标签list
def create_register_genre_list(userId,genre_list:List):
    # 假设这是你的ID列表和分数列表
    score_list = []
    score = 1
    for genre in  genre_list:
        score = 2 * score/3
        if score <= 0.1:
            score = 0.1
        score = round(score,3)
        
        score_list.append(score)
    
    for genre_id, score in zip(genre_list, score_list):
        set_genre_dao(userId,genre_id,score)

    # 使用字典推导式将两个列表合并成一个字典
    ratings_dict = {genre_id: score for genre_id, score in zip(genre_list, score_list)}
    return ratings_dict

# 转换表的内容如下,我希望genre_map中的字段可以按顺序通过这个表映射成1到18的int:
# Musical
# War
# Crime
# Romance
# Fantasy
# Drama
# Music
# Sci-Fi
# Action
# Comedy
# Biography
# Family
# Horror
# Short
# Documentary
# Film-Noir
# Animation
# Adventure
# News
# Mystery
# Sport
# History
# Thriller
# Western