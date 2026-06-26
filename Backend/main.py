from random import randrange
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

class post(BaseModel):
    title: str  
    content: str
    published: bool = True
    rating: Optional[int] = None

myposts = [{"title": "post 1", "content": "content of post 1", "published": True, "rating": 5, "id": 1},
           {"title": "post 2", "content": "content of post 2", "published": False, "id": 2}]

def find_post(id):
    for post in myposts:
        if post["id"] == id:
            return post

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Hello World !"}

@app.get("/posts")
def getPosts():
    return {"Posts": myposts}

@app.post("/posts")
def create_posts(Post: post):
    post_dict = Post.dict()
    post_dict["id"] = randrange(0, 1000000)
    myposts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if post:
        return {"post_detail": post}
    return {"message": "post not found"}

