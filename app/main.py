import psycopg2
import time
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
from psycopg2.extras import RealDictCursor
from . import models, scheemas
from .database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
def root():
    return {"detail": "Hello world."}


@app.get("/posts", response_model=List[scheemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    """ Retrieves all posts from the database. """

    posts = db.query(models.Post).all()

    return posts


@app.get("/posts/{id}", response_model=scheemas.PostResponse)
def get_one_post(id: int, db: Session = Depends(get_db)):
    """ Retrieves a single post from the database, given a post id. """

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found."
            )
    
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=scheemas.PostResponse)
def create_post(post: scheemas.PostCreate, db: Session = Depends(get_db)):
    """ Writes a new entry into the database, given a post. """

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    """ Deletes a post from the database, given a post id. """

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist."
            )
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=scheemas.PostResponse)
def update_post(id: int, updated_post: scheemas.PostCreate, db: Session = Depends(get_db)):
    """ Updates an entry from the database, given a post id and an updated post. """

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist."
            )
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=scheemas.UserResponse)
def create_user(user: scheemas.UserCreate, db: Session = Depends(get_db)):
    """ Adds a new user into the database, given the email and password. """
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    
    try:
        db.commit()

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Email already in use."
            )
    
    db.refresh(new_user)
    return new_user