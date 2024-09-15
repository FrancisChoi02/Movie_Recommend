import sqlite3
import json
from service.login_service import get_user_name
from fastapi import APIRouter, Path,Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from service.register_service import register_user,set_genre_by_userId
from service.login_service import get_user_by_name
from service.rating_service import add_rating_activity
from typing import List


# 我想在url中获取userId和movieID，请帮我修改一下post中使用的url 以及函数中的参数
rating_router = APIRouter()
@rating_router.post("/rating/{userId}/{movieId}")
async def movie_rating_controller(userId: str = Path(...), movieId: str = Path(...), rating_score: str = Form(...)):

    result = add_rating_activity(userId,movieId,rating_score)

    if result == 200:
        return json.dumps({"rating status": result})
    else:
        return json.dumps({"rating status": "There is something wrong with your action."})

