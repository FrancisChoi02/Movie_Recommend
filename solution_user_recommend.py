from service.recommend.movie_recommend import get_user_recommend_movie_list
from dao.user import set_user_recommend

def list_to_str(temp_list):
    # 提取列表中每个元组的第一个元素（ID），并转换为字符串列表
    id_list = [str(item[0]) for item in temp_list]
    # 将字符串列表连接成以 '|' 为分隔符的单一字符串
    return '|'.join(id_list)

def str_to_list(id_str):
    # 将字符串分割成字符串ID列表
    str_ids = id_str.split('|')
    # 将每个字符串ID转换为整数
    return [int(str_id) for str_id in str_ids]

# TODO 用户推荐表填值
# TODO 修改一下，不需要每次循环都导入Matrix
def initialize_user_recommend():
    for id in range(557,611):
        userId = str(id)

        print(userId)
        k=20
        count = 10
        initial_count = 8

        recommend_list = get_user_recommend_movie_list(userId,k,count)
        recommend_str = list_to_str(recommend_list)

        set_user_recommend(userId,recommend_str,initial_count)

# temp_list = [(3489, 44.44166021382308), (2571, 42.35670194738888), (1210, 41.2404385283491), (1676, 37.957852332014504), (2762, 37.13747538137952), (1527, 35.85295948623446), (1377, 32.46172974522316), (260, 31.87502714069855), (2081, 28.110439216292736), (2194, 27.513149659149313)]
# final = str_to_list(recommend_str)
initialize_user_recommend()