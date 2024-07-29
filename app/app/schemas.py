from pydantic import BaseModel

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
    pass

class Topic(TopicBase):
    id: int
    author_id: int
    room_id: int
    is_active: bool

    class Config:
        from_attributes = True