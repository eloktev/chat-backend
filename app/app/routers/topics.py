from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..db import get_db

router = APIRouter()

@router.get("/rooms/{room_id}/topics", response_model=list[schemas.Topic])
def read_topics(room_id: int, db: Session = Depends(get_db)):
    topics = crud.get_topics(db, room_id=room_id)
    return topics

@router.post("/rooms/{room_id}/topics", response_model=schemas.Topic)
def create_topic(room_id: int, topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    user_id = 1  # In a real app, you would get this from the authenticated user
    return crud.create_topic(db=db, topic=topic, user_id=user_id, room_id=room_id)

@router.put("/topics/{topic_id}/cancel", response_model=schemas.Topic)
def cancel_topic(topic_id: int, db: Session = Depends(get_db)):
    return crud.cancel_topic(db=db, topic_id=topic_id)