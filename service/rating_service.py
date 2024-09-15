from dao.rating import(
    get_rating_record,
    delete_rating_record,
    update_rating_record,
    add_rating_record,
    get_rating_record_times,
)
from dao.user import(
    upgrade_genre_with_count_dao,
)
from service.movie_service import (
    get_genreId,
    get_genre_list_from_movie,
)

# 获取用于对当前电影的评分分值
def get_rating_information(userId, movieId):
    result = get_rating_record(userId,movieId)

    score = 0
    if result:
        score = result[2]
    
    return score


# 评分逻辑
# 在执行新增/更新/删除评分操作之前，获取电影的属性列表，然后获取评分的电影的数量，将“评分*权重/(评分数量+1)”，通过电影属性列表重新映射回属性对应的id，像对应的属性添加新增的score
def add_rating_activity(userId, movieId, rate):

    # 获取之前的评价行为
    result = get_rating_record(userId, movieId)
    movie_counts = get_rating_record_times(userId)

    # 如果已经评价过
    if result:
        existing_rate = result[2]
        print(f"rating{result[2]}")
        if rate == existing_rate:
            # 如果评分相同，则删除这条评分
            delete_rating_record(userId,movieId)
        else:
            # 如果评分不同，则更新评分
            update_rating_record(userId,movieId,rate)
    else:
        # 如果没有评价过，则直接添加一条评价数据
        add_rating_record(userId, movieId,rate)
        

    genre_list = get_genre_list_from_movie(movieId,rate)
    
    # 对每个属性进行处理
    for genre in genre_list:
        # 假设有一个函数根据电影属性重新映射回属性对应的id
        genre_id = get_genreId(genre)
        if genre_id > 0:
            # 假设有一个函数来处理和更新属性评分
            upgrade_genre_with_count_dao(userId, genre_id, rate, movie_counts)

    return 200

