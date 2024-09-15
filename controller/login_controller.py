import os
import ast
import sqlite3
from pathlib import Path
from service.login_service import get_user_name
from fastapi import APIRouter, HTTPException, Form, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent/'.env')




from fastapi.responses import JSONResponse
login_router = APIRouter()
@login_router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):

    user_info_raw = get_user_name(username)
    
    if not user_info_raw:
        return "不存在该用户"
    
    stored_password = user_info_raw[2]  
    if password != stored_password:
        return "密码不正确"
    
    # 如果密码匹配，返回用户信息
    user_info = {"id": user_info_raw[0], "username": user_info_raw[1]}

    return user_info


