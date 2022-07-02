import imp
import jwt
from fastapi import Header, HTTPException
from jwt.exceptions import ExpiredSignatureError, DecodeError
from typing import Union

# https://fastapi.tiangolo.com/tutorial/header-params/
# https://stackoverflow.com/questions/68231936/python-fastapi-how-can-i-get-headers-or-a-specific-header-from-my-backend-api


async def isAuth(Authorization: Union[str, None] = Header()):
    # print("*" * 200)
    # print(Authorization)
    # print("*" * 200)
    print("isAuth")
    jwtToken = Authorization
    JWT_SECRET = "F2dN7x8HVzBWaQuEEDnhsvHXRWqAR63z"
    JWT_ALGORITHM = "HS256"
    if not jwtToken.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication Error")
    token = jwtToken.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        userId = payload['id']
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Authentication Error")
    except DecodeError:
        raise HTTPException(status_code=401, detail="Authentication Error")    
    return dict(Authorization=f"Bearer {token}", userId = userId)

