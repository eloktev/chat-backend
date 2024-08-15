from pydantic import BaseModel

class UserBase(BaseModel):
    id: int
    fingerprint: str
    minchat_id: str
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    fingerprint: str
    user_agent : str
    browser : str
    os : str
    language : str

class RoomBase(BaseModel):
    name: str

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int

    class Config:
        from_attributes = True

class TopicBase(BaseModel):
    caption: str

class TopicCreate(TopicBase):
    minchat_id: str
    user_id: str

class Topic(TopicBase):
    id: int
    author_id: int
    room_id: int
    status: str
    respondee_id: int | None
    chat_id: str

    class Config:
        from_attributes = True
