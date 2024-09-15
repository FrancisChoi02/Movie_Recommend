from dao.rating import get_rating_by_userId
from dao.movie import get_movie_with_movieId_dao
from dao.common import(
    split_genre_to_list,
    convert_genre_to_dict,
)
from service.movie_service import get_genre_score_from_movie,set_genre,get_genre_list_dict_from_movie

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

create_user_genre_from_rating()