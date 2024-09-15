# 项目文档


# 环境依赖

## Anaconda

下载一个Anaconda

```python
conda create -n **prompt** python=3.10
```

进入MOVIE_RECOMMEND的文件夹

```python
cd MOVIE_RECOMMEND
```

```python
pip install -r requirment.txt
```

## Docker

构建chromaDB

```python
sudo docker run -dp 1235:8000 --name movieChroma chromadb/chroma:0.4.23
```

### .env文件

项目启动需要从Azure OpenAI 获取相应Deployment的API（GPT-4 与 text-embedding-ada-2 对应的ebd） 

```python
COLLECTION_MULTI_SCOPE=Just_For_Test
COLLECTION_MOVIE = Recommend_Movie
COLLECTION_DIRECTOR = Recommend_Director
COLLECTION_STAR = Recommend_Star
COLLECTION_MIX = Recommend_Mix

CHROMA_PORT = 1235

OPENAI_API_BASE_VISION=
OPENAI_API_KEY_VISION=
DEPLOYMENT_VISION=gpt4v
DEPLOYMENT_GPT4=gpt4
OPENAI_API_TYPE=azure
OPENAI_API_VERSION=2023-07-01-preview

CHROMA_HOST=0.0.0.0
CHROMA_PORT=1235
APP_PORT=3315

OPENAI_API_BASE=
OPENAI_API_KEY=
DEPLOYMENT_EBD=ebd
DEPLOYMENT_GPT4=gpt4
OPENAI_API_TYPE=azure
OPENAI_API_VERSION=2023-07-01-preview

COLLECTION_NAME=Test_For_PNG
COLLECTION_DETAILS=PNG_Project_Details
COLLECTION_SCOPE_ENHANCED=PNG_Scope_selection_Enhanced
COLLECTION_MULTI_SCOPE=PNG_Multi_Scope
COLLECTION_COUNTRY=PNG_country_selection_step1
COLLECTION_SCOPE=PNG_Scope_selection
COLLECTION_REQUEST=PNG_Scope_request
COLELCTION_TEST_NAME=PNG_Test_Name
```

# 数据集初始化

- 在MOVIE_RECOMMEND的文件夹中

```python
cd service
cd data_pre_processing
python table_construction_service.py
python data_construction_service.py
```

# 后端

### 架构介绍

- controller
    
    存放路由处理逻辑
    
- dao
    
    数据库CRUD相关代码
    
- entity
    
    数据类相关代码
    
- service
    
    逻辑处理相关代码
    
- service/data_preproccessing
    
    数据预处理
    
- service/evaluation
    
    协同过滤算法评测代码
    
- service/recommend
    
    推荐逻辑
    
- service/web_scraping
    
    爬虫代码
    
- front_end_test
    
    前端相关展示页面
    
- static
    
    相关csv数据
    

## API解释

### **1. 登录API**

- **URL**: **`/login`**
- **方法**: POST
- **描述**: 此API用于用户登录。它接受用户名和密码，验证用户是否存在以及密码是否正确，并返回用户信息。
- **参数**:
    - **`username`** (string, required): 用户的用户名。
    - **`password`** (string, required): 用户的密码。
- **成功响应**:
    - **内容**: 用户的基本信息，如 **`{ "id": "1", "username": "sampleuser" }`**
- **错误响应**:
    - **内容**: **`"不存在该用户"`**
    - **内容**: **`"密码不正确"`**

### **2. 电影搜索API**

- **URL**: **`/movie_search`**
- **方法**: POST
- **描述**: 根据输入的字符串搜索相关电影。如果输入符合特定条件（通过调用**`call_gpt`**判断），则使用**`get_movie_with_search_name`**方法搜索电影；否则使用生成式推荐**`get_generative_recommend`**。
- **参数**:
    - **`search_str`** (string, required): 搜索的关键词。
- **成功响应**:
    - **内容**: 返回电影列表或提示没有结果的信息，如 **`{ "movie_search_result": [{"title": "Inception", "year": "2010"}] }`**
- **错误响应**:
    - **内容**: **`{"movie_search_result": "There is no result"}`**

### **3. 电影详细信息API**

- **URL**: **`/movie/{movie_id}`**
- **方法**: GET
- **描述**: 获取指定ID的电影详细信息，包括类似电影的推荐。
- **参数**:
    - **`movie_id`** (string, required): 电影的ID。
- **成功响应**:
    - **内容**: 包含电影详细信息及相似电影的JSON数据，如 **`{ "movie": {"title": "Inception", "year": "2010"}, "similar_movies": [{"title": "The Matrix", "year": "1999"}] }`**
- **错误响应**:
    - **内容**: **`"There is no relevant movie information"`**

### **4. 电影评分API**

- **URL**: **`/rating/{userId}/{movieId}`**
- **方法**: POST
- **描述**: 用户为指定电影打分。
- **参数**:
    - **`userId`** (string, required): 用户ID。
    - **`movieId`** (string, required): 电影ID。
    - **`rating_score`** (string, required): 评分值。
- **成功响应**:
    - **内容**: **`{"rating status": 200}`**
- **错误响应**:
    - **内容**: **`{"rating status": "There is something wrong with your action."}`**
    

### **5. 注册API**

- **URL**: **`/register`**
- **方法**: POST
- **描述**: 新用户注册。验证用户名是否已存在，密码是否一致，并创建新用户。
- **参数**:
    - **`username`** (string, required): 用户名。
    - **`password`** (string, required): 密码。
    - **`ConfirmPassword`** (string, required): 确认密码。
- **成功响应**:
    - **内容**: 返回新注册用户的信息，如 **`{ "id": "2", "username": "newuser" }`**
- **错误响应**:
    - **内容**: **`"该用户已存在"`**
    - **内容**: **`"密码不一致"`**

### **6. 设置用户喜好电影类型API**

- **URL**: **`/set_genre`**
- **方法**: POST
- **描述**: 为用户设置喜好的电影类型。此API接受用户ID和一个包含电影类型的字符串列表，更新用户的偏好设置。
- **参数**:
    - **`userId`** (string, required): 用户ID。
    - **`genre_list`** (string, required): 用户喜好的电影类型，以字符串列表形式提供。
- **成功响应**:
    - **内容**: 返回更新后的用户状态信息，如 **`{ "id": "1", "username": "updated" }`**。这里**`username`**字段返回的是**`set_genre_by_userId`**函数的结果，代表操作结果或用户的状态。

### **7. 根据电影类型ID获取电影列表API**

- **URL**: **`/movie_genre/{genre_id}`**
- **方法**: GET
- **描述**: 根据提供的电影类型ID获取相应类型的电影列表。此API首先将类型ID转换为对应的类型名称，然后根据该名称获取电影列表。
- **参数**:
    - **`genre_id`** (string, required): 电影类型的ID。
- **成功响应**:
    - **内容**: 返回匹配指定类型的电影列表。例如，**`{"genre_movie": [{"title": "Inception", "year": "2010"}, {"title": "Interstellar", "year": "2014"}]}`**。响应中的**`genre_movie`**键包含一个电影对象列表，每个电影对象提供了电影的详细信息。
- **错误响应**:
    - **内容**: **`"Genre not found"`**

### **8. 用户推荐电影列表API**

- **URL**: **`/movie_recommend/{user_id}`**
- **方法**: GET
- **描述**: 根据用户ID提供推荐电影列表。该API首先获取系统的顶级推荐电影，然后根据用户的历史和偏好获取个性化推荐电影。
- **参数**:
    - **`user_id`** (string, required): 用户的ID。
- **成功响应**:
    - **内容**: 返回包含顶级推荐电影和个性化推荐电影的列表。例如，**`{"movie": [{"title": "Avatar", "year": "2009"}], "similar_movies": [{"title": "Star Wars", "year": "1977"}]}`**。这里**`movie`**键包含顶级推荐的电影列表，**`similar_movies`**键包含基于用户偏好的推荐电影列表。
- **错误响应**:
    - 如果用户ID无效或不存在，返回：
    - **内容**: **`"User not found"`**

## 启动说明

前后端分别需要两个server

server 1： 

```python
cd MOVIE_RECOMMEND
python app.py
```

server 2:

```python
cd MOVIE_RECOMMEND
cd front_end_test
cd react_test
npm start
```