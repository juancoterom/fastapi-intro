from app.database.database import get_db
from app.database.models import Post, User, Vote
from app.libs.oauth2 import get_current_user
from .schemas.schemas import VoteCreate

from fastapi import status, APIRouter, HTTPException, Response, Depends
from sqlalchemy.orm import Session


router = APIRouter(prefix="/votes", tags=['Votes'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_vote(
    vote: VoteCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict[str, str]:
    """ Writes vote into database, given the current user and post. """

    # Check if post exists in database.
    post_query = db.query(Post).filter(Post.id == vote.post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} not found."
        )

    # Retrieve data from votes table.
    vote_query = db.query(Vote).filter(
        Vote.user_id == current_user.id,
        Vote.post_id == vote.post_id
    )
    found_vote = vote_query.first()
    
    # Add vote if it does not already exist in database.
    if found_vote:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {current_user.id} has already voted on post {vote.post_id}."
        )
    
    new_vote = Vote(user_id=current_user.id, post_id=vote.post_id)
    db.add(new_vote)
    post_query.update({Post.votes: post.votes+1}, synchronize_session=False)
    db.commit()

    return {
        "message": f"Successfully added vote on post {vote.post_id}."
    }


@router.delete("/", status_code=status.HTTP_201_CREATED)
def delete_vote(
    vote: VoteCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Response:
    """ Deletes vote from database, given the current user and post. """

    # Check if post exists in database.
    post_query = db.query(Post).filter(Post.id == vote.post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} not found."
        )

    # Retrieve data from votes table.
    vote_query = db.query(Vote).filter(
        Vote.user_id == current_user.id,
        Vote.post_id == vote.post_id
    )
    found_vote = vote_query.first()

    # Delete vote if it exists in database.
    if not found_vote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vote does not exist."
        )
    
    vote_query.delete(synchronize_session=False)
    post_query.update({Post.votes: post.votes-1}, synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)