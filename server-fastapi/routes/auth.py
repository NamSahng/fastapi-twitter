import bcrypt
import jwt
from fastapi import APIRouter
from starlette.responses import JSONResponse
from starlette.requests import Request
from datetime import datetime, timedelta

import data.auth as userRepository

from middleware.auth import isAuth

router = APIRouter(prefix='/auth')

JWT_SECRET = "F2dN7x8HVzBWaQuEEDnhsvHXRWqAR63z"
JWT_ALGORITHM = "HS256"
bcryptSaltRounds = 12

@router.post("/signup")
async def signUp(request: Request):
    req = await request.json()
    found = await userRepository.findByUsername(req['username'])
    if found:
        return JSONResponse(status_code=400, content=dict(msg="username exist!"))
    hashed = bcrypt.hashpw(req['password'].encode("utf-8"), bcrypt.gensalt(bcryptSaltRounds))
    req['password'] = hashed
    userId = await userRepository.createUser(req)
    token = createAccessToken(data = dict(id=userId) , )
    resBody = dict(token=f"Bearer {token}", username=req['username'])
    return JSONResponse(status_code=201, content=resBody)


@router.post("/login")
async def login(request: Request):
    req = await request.json()
    user = await userRepository.findByUsername(username=req['username'])
    if not user:
        return JSONResponse(status_code=401, content=dict(msg="Invalid user or password"))
    isValid = bcrypt.checkpw(req['password'].encode("utf-8"), user['password'].encode("utf-8"))
    if not isValid:
        return JSONResponse(status_code=401, content=dict(msg="Invalid user or password"))
    token = createAccessToken(dict(id=user['id']))
    resBody = dict(token=f"Bearer {token}", username=user['username'])
    return JSONResponse(status_code=200, content=resBody)


@router.get("/me")
async def me(req : Request):
    token = await isAuth(req)
    if isinstance(token, str):
        return JSONResponse(status_code=401, content=dict(msg="User not found"))
    found = await userRepository.findById(token['userId'])
    if not found:
        return JSONResponse(status_code=404, content=dict(msg="User not found"))
    resBody = dict(token = token['Authorization'], username = found['username'])
    return JSONResponse(status_code=200, content=resBody)
    

def createAccessToken(data: dict = None, expires_delta: int = 1):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

