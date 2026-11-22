from random import randrange
from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response
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

def find_index_post(id):
    for i, p in enumerate(myposts):
        if p["id"] == id:
            return i
    return None

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Hello World !"}

@app.get("/posts")
def getPosts():
    return {"Posts": myposts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(Post: post):
    post_dict = Post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    myposts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"message": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    myposts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, Post: post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_dict = Post.model_dump()
    post_dict['id'] = id
    myposts[index] = post_dict
    return {"data": post_dict}