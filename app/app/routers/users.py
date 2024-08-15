from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, models, schemas
from ..db import get_db

router = APIRouter()

@router.post("/users", response_model=schemas.UserBase)
def get_or_create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user_if_not_exists(db, user=user)
