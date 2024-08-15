from sqlalchemy.orm import Session
from . import models, schemas
from app.minchat_service import MinchatService
from loguru import logger

min_srvc = MinchatService()

def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()

def get_rooms(db: Session):
    return db.query(models.Room).all()

def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(name=room.name)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_topic(db: Session, topic_id: int):
    return db.query(models.Topic).filter(models.Topic.id == topic_id).first()

def get_topics(db: Session, room_id: int):
    return db.query(models.Topic).filter(models.Topic.room_id == room_id, models.Topic.status == "CREATED").all()

def get_minchat_user_id_by_user_id(db:Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    return db_user.minchat_id

def get_fingerprint_by_user_id(db:Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    return db_user.fingerprint


def create_user_if_not_exists(db: Session, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.fingerprint == user.fingerprint).first()
    if db_user is None:
        logger.info(f"User with firngerprint {user.fingerprint} not found")
        min_user_id = min_srvc.create_user(user.fingerprint)
        db_user = models.User(fingerprint=user.fingerprint, user_agent=user.user_agent, browser=user.browser, os=user.os, language=user.language , minchat_id=min_user_id)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    elif db_user.minchat_id is None:
        logger.info(f"User with firngerprint {user.fingerprint} found, but minchat_id is None")
        min_user_id = min_srvc.create_user(user.fingerprint)
        db_user.minchat_id = min_user_id
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user

def create_topic(db: Session, topic: schemas.TopicCreate, room_id: int):
    # create_user_if_not_exists(db, user_id)
    min_chat_id = min_srvc.create_chat(user_id=topic.minchat_id, title=topic.caption)
    
    db_topic = models.Topic(caption=topic.caption, author_id=topic.user_id, room_id=room_id, chat_id=min_chat_id)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    
    return db_topic

def mark_topic_active(db:Session, topic_id: int):
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if db_topic:
        db_topic.status = "ACTIVE"
        db.add(db_topic)
        db.commit()
        db.refresh(db_topic)
        return db_topic


def cancel_topic(db: Session, topic_id: int):
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    min_srvc.send_message(db_topic.chat_id, message="Partner left the chat")
    db_topic.status = "CLOSED"
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def get_topic(db: Session, topic_id: int):
    return db.query(models.Topic).filter(models.Topic.id == topic_id).first()


def add_respondee(db: Session, topic_id: int, respondee_id : int):
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if db_topic and db_topic.respondee_id is None:
        db_topic.respondee_id = respondee_id
        db_topic.status = "ACTIVE"
        db.add(db_topic)
        min_srvc.add_user_to_chat(chat_id = db_topic.chat_id, minchat_user_id=get_minchat_user_id_by_user_id(db, respondee_id), fingerprint=get_fingerprint_by_user_id(db, respondee_id))
        db.commit()
        db.refresh(db_topic)
    return db_topic
    # return None