from .. import models, schemas, oauth2
from ..database import get_db
from fastapi import status, HTTPException, Response, APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user)
    ):
    """ Retrieves all posts from the database. """

    posts = db.query(models.Post).all()

    return posts


@router.get("/{id}", response_model=schemas.PostResponse)
def get_one_post(
    id: int, 
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user)
    ):
    """ Retrieves a single post from the database, given a post id. """

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found."
            )
    
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    user_id: int = Depends(oauth2.get_current_user)
    ):
    """ Writes a new entry into the database, given a post. """

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session = Depends(get_db), 
    user_id: int = Depends(oauth2.get_current_user)
    ):
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


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int, 
    updated_post: schemas.PostCreate, 
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user)
    ):
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