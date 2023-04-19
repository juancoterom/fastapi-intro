from .. import models, schemas, oauth2
from ..database import get_db
from fastapi import status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session


router = APIRouter(prefix="/votes", tags=['Votes'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.VoteCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(oauth2.get_current_user)
    ) -> dict[str, str]:
    """ Writes vote into database, given the current user and post. """

    # Check if post exists in database.
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} not found."
            )

    # Retrieve data from votes table.
    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id,
        models.Vote.post_id == vote.post_id
        )
    found_vote = vote_query.first()
    
    # Check if vote should be added or deleted.
    if(vote.dir == 1):
        # Add vote if it does not already exist in database.
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on post {vote.post_id}."
                )
        
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()

        return {
            "message": "Successfully added vote."
        }
        
    else:
        # Delete vote if it exists in database.
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist."
                )
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {
            "message": "Successfully deleted vote."
        }