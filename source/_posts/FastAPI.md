---
title: FastAPI
date: 2026-06-15 12:13:40
tags: ["FastAPI"]
categories: ["Agent开发"] 
---

>学习资源： [FastAPI官方文档](https://fastapi.tiangolo.com/tutorial/)
> 

# 环境配置
```bash
pip install "fastapi[standard]"
```

# First Step
## 简单示例
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def hello():
    return {"message": "hello world"}
```
```bash
(agentlearning) PS D:\code\PythonProject> fastapi dev fast_api.py --port 8001  #规定端口号

   FastAPI   Starting development server 🚀
 
             Searching for package file structure from directories with __init__.py files
             Importing from D:\code\PythonProject
 
    module   🐍 fast_api.py
 
      code   Importing the FastAPI app object from the module with the following code:
 
             from fast_api import app
 
       app   Using import string: fast_api:app
 
    server   Server started at http://127.0.0.1:8001
    server   Documentation at http://127.0.0.1:8001/docs
 
       tip   Running in development mode, for production use: fastapi run
 
             Logs:
 
      INFO   Will watch for changes in these directories: ['D:\\code\\PythonProject']
      INFO   Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
      INFO   Started reloader process [2252] using WatchFiles
      INFO   Started server process [6800]
      INFO   Waiting for application startup.
      INFO   Application startup complete.
      INFO   127.0.0.1:51683 - "GET / HTTP/1.1" 200
      INFO   127.0.0.1:51683 - "GET /docs HTTP/1.1" 200
      INFO   127.0.0.1:51683 - "GET /openapi.json HTTP/1.1" 200
      INFO   127.0.0.1:53840 - "GET / HTTP/1.1" 200
```

## 指定app位置的不同方式
命令行直接指定
```bash
fastapi dev fast_api.py
fastapi dev --entrypoint fast_api:app
```

可以在 `pyproject.toml`文件中规定app的位置:
```
[tool.fastapi]
entrypoint="fast_api:app"
```
此时就不用明确指定运行哪个文件:
```bash
fastapi dev
```
## 部署
可以把FastAPI app部署到 `FastAPI Cloud`
```bash
fastapi deploy
```

## 常用operatio

- GET : read
- PUSH : update
- DELETE : delete
- POST : create

## 创建`a path operation decorator`
`@app.get("/")`的作用是告诉FastAPI:
1. 要处理的路径是"/"
2. 使用get装饰器

其他类似操作:
- @app.post()
- @app.put()
- @app.delete()

## 定义`path operation function`
即如果访问上面创建的路径,应该采取什么动作(执行什么函数)
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```
如果使用GET访问/路径,会执行root函数,返回"Hello World"字符串

## Path Parameters
对于路径可以搭配不同的参数使用

1. 无参数
    ```python
    @app.get("/")
    ```
2. 定义变量
    ```python
    @app.get("/item/{item_id}")
    async def get_item(item_id:str):
        return {"item_id":item_id}
    ```
    item_id这个变量会通过路径传给函数
3. 