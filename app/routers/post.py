from .. import models, schemas
from ..database import get_db
from fastapi import status, HTTPException, Response, APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List


router = APIRouter()


@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    """ Retrieves all posts from the database. """

    posts = db.query(models.Post).all()

    return posts


@router.get("/posts/{id}", response_model=schemas.PostResponse)
def get_one_post(id: int, db: Session = Depends(get_db)):
    """ Retrieves a single post from the database, given a post id. """

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found."
            )
    
    return post


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """ Writes a new entry into the database, given a post. """

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
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