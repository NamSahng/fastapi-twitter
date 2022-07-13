import jwt
import bcrypt
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
import data.auth as userRepository
from database import schemas
from middleware.auth import isAuth


# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/
router = APIRouter()

JWT_SECRET = "F2dN7x8HVzBWaQuEEDnhsvHXRWqAR63z"
JWT_ALGORITHM = "HS256"
bcryptSaltRounds = 12

@router.post("/signup", response_model=schemas.UserOut, status_code=201)
async def signUp(newUser: schemas.UserCreate, db : Session = Depends(get_db)):
    found = await userRepository.findByUsername(db, newUser.username)
    if found:
        raise HTTPException(status_code=400, detail="Username exists")
    hashed = bcrypt.hashpw(newUser.password.encode("utf-8"), bcrypt.gensalt(bcryptSaltRounds))
    newUser.password = hashed
    createdUser = await userRepository.createUser(db, newUser)
    token = createAccessToken(data = dict(id=createdUser.id) , )
    return dict(token=f"Bearer {token}", username=newUser.username)


@router.post("/login", response_model=schemas.UserOut, status_code=200)
async def login(loginUser: schemas.UserBase, db : Session = Depends(get_db)):
    found = await userRepository.findByUsername(db, username=loginUser.username)
    if not found:
        raise HTTPException(status_code=400, detail="Invalid user or password")
    isValid = bcrypt.checkpw(loginUser.password.encode("utf-8"), found.password.encode("utf-8"))
    if not isValid:
        raise HTTPException(status_code=400, detail="Invalid user or password")
    token = createAccessToken(dict(id=found.id))    
    return dict(token=f"Bearer {token}", username=loginUser.username)


@router.get("/me", response_model=schemas.UserOut, status_code=200)
async def me(token : dict = Depends(isAuth), db : Session = Depends(get_db)):
    found = await userRepository.findById(db, token['userId'])
    if not found:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(token = token['Authorization'], username = found.username)
    

def createAccessToken(data: dict = None, expires_delta: int = 1):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

