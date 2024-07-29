from sqlalchemy.orm import Session
from . import models, schemas

def get_rooms(db: Session):
    return db.query(models.Room).all()

def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(name=room.name)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_topics(db: Session, room_id: int):
    return db.query(models.Topic).filter(models.Topic.room_id == room_id, models.Topic.is_active == True).all()

def create_user_if_not_exists(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        user = models.User(id=user_id, session_id=f'session_{user_id}')
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def create_topic(db: Session, topic: schemas.TopicCreate, user_id: int, room_id: int):
    create_user_if_not_exists(db, user_id)
    db_topic = models.Topic(caption=topic.caption, author_id=user_id, room_id=room_id)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def cancel_topic(db: Session, topic_id: int):
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    db_topic.is_active = False
    db.commit()
    return db_topic

def get_topic(db: Session, topic_id: int):
    return db.query(models.Topic).filter(models.Topic.id == topic_id).first()

def mark_topic_inactive(db: Session, topic_id: int):
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if db_topic:
        db_topic.is_active = False
        db.commit()
        db.refresh(db_topic)
        return db_topic
    return None