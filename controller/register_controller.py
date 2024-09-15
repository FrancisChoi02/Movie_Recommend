import sqlite3
from service.login_service import get_user_name
from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from service.register_service import register_user,set_genre_by_userId
from service.login_service import get_user_by_name
from typing import List


register_router = APIRouter()
register_genre_router = APIRouter()

@register_router.post("/register")
async def register(username: str = Form(...), password: str = Form(...), ConfirmPassword: str = Form(...)):

    user_info_raw = get_user_name(username)
    
    if  user_info_raw:
        return "该用户已存在"
    
    if password != ConfirmPassword:
        return "密码不一致"
    
    # set_user_regist
    # 获取用户ID
    new_user_id = register_user(username,password)


    # 如果密码匹配，返回用户信息
    user_info = {"id": new_user_id, "username": username}

    return user_info


# Genre_list 设置
@register_genre_router.post("/set_genre")
async def register_genre(userId: str=Form(...), genre_list: str=Form(...) ):

    # set_genre
    result = set_genre_by_userId(userId,genre_list)

    user_status = {"id": userId, "username": result}

    return user_status

