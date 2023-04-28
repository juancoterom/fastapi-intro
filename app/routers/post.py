from app.database.database import get_db
from app.database.models import Post
from app.libs.oauth2 import get_current_user
from .schemas.schemas import PostCreate, PostResponse, UserResponse

from fastapi import status, HTTPException, Response, APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional


router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model=List[PostResponse])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10, skip: int = 0, search: Optional[str] = ""
) -> List[Post]:
    """ Retrieves all posts from the database. """

    posts = db.query(Post).filter(
        Post.title.contains(search)
    ).limit(limit).offset(skip).all()
    
    return posts


@router.get("/{id}", response_model=PostResponse)
def get_one_post(
    id: int, 
    db: Session = Depends(get_db),
) -> Post:
    """ Retrieves a post from the database, given a post id. """

    post = db.query(Post).filter(Post.id == id).first()

    # Check if post exists in the database.
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found."
        )
    
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user)
) -> Post:
    """ Writes a new entry into the database, given a post. """

    new_post = Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user)
) -> Response:
    """ Deletes a post from the database, given a post id. """

    # Retrieve post from database.
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    # Check if post exists in the database.
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist."
        )
    
    # Check if current user is the owner of the post.
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to perform requested action."
        )
    
    # Delete post and save changes.
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostResponse)
def update_post(
    id: int, 
    updated_post: PostCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
) -> Post:
    """ Updates an entry from the database, given a post id and an updated post. """

    # Retrieve post from database.
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    # Check if post exists in the database.
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist."
        )
    
    # Check if current user is the owner of the post.
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to perform requested action."
        )
    
    # Update post and save changes.
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()