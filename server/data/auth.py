from typing import Union
from sqlalchemy.orm import Session
from database.models import Users
from database import schemas


async def findByUsername(db: Session, username: str):
    return db.query(Users).filter(Users.username == username).first()


async def findById(db: Session, id: int):
    return db.query(Users).filter(Users.id == id).first()


async def createUser(db: Session, user: schemas.UserCreate):
    newUser = Users(**user.dict())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

