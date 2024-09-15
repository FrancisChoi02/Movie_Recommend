import os
import uvicorn
from dotenv import load_dotenv
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from controller.login_controller import login_router
from controller.register_controller import register_router
from controller.movie_controller import movie_router,movie_genre_router
from service.data_preprocessing.matrix_construction_service import refresh_rating_matrix,refresh_userGenre_matrix
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

#跨域资源共享规则
app.add_middleware(    
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],)

app.include_router(login_router)
app.include_router(register_router)
app.include_router(movie_router)
app.include_router(movie_genre_router)


# 定时更新推荐矩阵
# 创建后台线程并启动
thread_rating = threading.Thread(target=refresh_rating_matrix)
thread_userGenre = threading.Thread(target=refresh_userGenre_matrix)

thread_rating.start()
thread_userGenre.start()



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('APP_PORT')))