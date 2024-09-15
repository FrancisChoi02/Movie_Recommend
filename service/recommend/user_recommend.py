import pickle
from service.recommend.common_recommend import(
    read_genre_data,
    get_userItem_dict,
)

def get_user_genre_similarity_matrix():
    with open('D:\\Movie_Recommend\\static\\user_genre_similarity_matrix.pkl', 'rb') as f:
        user_genre_similarity_matrix = pickle.load(f)
    return user_genre_similarity_matrix


# 根据userId直接返回推荐用户id
def recommend_user(userId,selected_genres_dict_raw,item_similarity_matrix,k,count):
    rank = dict()

    selected_genres_dict = selected_genres_dict_raw[userId]

    for genre, rating in selected_genres_dict.items():
        # 相似用户和权重
        for related_genre, w in sorted(item_similarity_matrix[genre].items(), key=lambda x: x[1],
                                        reverse=True)[:k]:
            if related_genre in selected_genres_dict.keys():
                continue
            rank.setdefault(related_genre, 0)
            rank[related_genre] += w * float(rating)
    result = sorted(rank.items(), key=lambda x: x[1], reverse=True)[:count]
    return result[0]



# 根据UserId获取用户推荐电影列表
def get_recommend_userId(userId,k,count):
    rating_result = read_genre_data()
    matrix = get_user_genre_similarity_matrix()
    
    
    # 获取用户评价的电影，根据用户评价电影进行相似推荐
    selected_genres_dict = get_userItem_dict(rating_result)

    recommend_user_raw = recommend_user(userId,selected_genres_dict,matrix,k,count)

    return recommend_user_raw
