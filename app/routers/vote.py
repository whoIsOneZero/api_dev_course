from fastapi import Response, status, HTTPException, Depends, APIRouter
from models import models
from schemas import schemas
from sqlalchemy.orm import Session
from database.db import get_db
from database import oauth2, db

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(db.get_db), current_user: int = Depends(oauth2.get_current_user)):

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):  # cast vote
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {
                                current_user.id} has already voted on post {vote.post_id}")

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:  # delete vote
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully removed vote"}