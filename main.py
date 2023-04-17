from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def root():
    return {"message": "Hello world."}

@app.get("/posts")
def get_posts():
    return {"message": "This is your posts."}

@app.post("/posts")
def post_posts(new_post: Post):
    print(new_post)
    return {"data": "new post"}