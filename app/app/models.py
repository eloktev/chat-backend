from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db import Base
import enum


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    fingerprint = Column(String, unique=True, index=True) 
    minchat_id = Column(String, unique=True, index=True) 
    user_agent = Column(String) 
    browser = Column(String) 
    os = Column(String) 
    language = Column(String) 

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    caption = Column(String, index=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))
    status = Column(String, default="CREATED")
    respondee_id =Column(Integer, ForeignKey('users.id'), nullable=True)
    chat_id = Column(String, nullable=True)

    author = relationship("User", foreign_keys=[author_id])
    respondee = relationship("User", foreign_keys=[respondee_id])
    room = relationship("Room")

