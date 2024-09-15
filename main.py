# 保存为 main.py
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允许跨域请求，因为前端和后端在开发时可能会运行在不同的端口上
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    # 这里只是一个示例，实际应用中应该有更复杂的逻辑来验证用户名和密码
    if username == "admin" and password == "admin":
        return {"message": "登录成功"}
    else:
        raise HTTPException(status_code=400, detail="用户名或密码错误")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)