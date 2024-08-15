from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..db import get_db

router = APIRouter()

@router.get("/rooms/{room_id}", response_model=schemas.Room)
def read_rooms(room_id: int, db: Session = Depends(get_db)):
    rooms = crud.get_room(db, room_id=room_id)
    return rooms

@router.get("/rooms", response_model=list[schemas.Room])
def read_rooms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    rooms = crud.get_rooms(db)
    return rooms

@router.post("/rooms", response_model=schemas.Room)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_room(db=db, room=room)