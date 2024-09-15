from dao.user import get_user_by_name

# 根据用户名字获取用户
def get_user_name(username:str):
    user_raw_info = get_user_by_name(username)
    return user_raw_info