import os
from dotenv import load_dotenv
import jwt
from fastapi import Header, HTTPException
from jwt.exceptions import ExpiredSignatureError, DecodeError
from typing import Union

load_dotenv()

# https://fastapi.tiangolo.com/tutorial/header-params/
# https://stackoverflow.com/questions/68231936/python-fastapi-how-can-i-get-headers-or-a-specific-header-from-my-backend-api


async def isAuth(Authorization: Union[str, None] = Header()):
    jwtToken = Authorization
    jwtSecret = os.getenv("JWT_SECRET")
    jwtAlrgorithm = os.getenv("JWT_ALGORITHM")
    if not jwtToken.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication Error")
    token = jwtToken.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, key=jwtSecret, algorithms=[jwtAlrgorithm])
        userId = payload['id']
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Authentication Error")
    except DecodeError:
        raise HTTPException(status_code=401, detail="Authentication Error")    
    return dict(Authorization=f"Bearer {token}", userId = userId)

