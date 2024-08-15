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
    return crud.create_topic(db=db, topic=topic, room_id=room_id)

@router.get("/topics/{topic_id}", response_model=schemas.Topic)
def read_topic(topic_id: int, db: Session = Depends(get_db)):
    return crud.get_topic(db=db, topic_id=topic_id)

@router.put("/topics/{topic_id}/cancel", response_model=schemas.Topic)
def cancel_topic(topic_id: int, db: Session = Depends(get_db)):
    return crud.cancel_topic(db=db, topic_id=topic_id)

@router.put("/topics/{topic_id}/add_respondee", response_model=schemas.Topic)
def add_respondee(topic_id: int, respondee_id: int, db: Session = Depends(get_db)):
    crud.mark_topic_active(db=db, topic_id=topic_id)
    return crud.add_respondee(db=db, topic_id=topic_id, respondee_id=respondee_id)