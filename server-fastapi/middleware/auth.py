import imp
import jwt
from fastapi import Request
from starlette.responses import JSONResponse
from jwt.exceptions import ExpiredSignatureError, DecodeError
import data.auth as userRepository

# https://fastapi.tiangolo.com/tutorial/header-params/
# https://stackoverflow.com/questions/68231936/python-fastapi-how-can-i-get-headers-or-a-specific-header-from-my-backend-api

# @app.post('/city')
# async def create_city(body: BodyModel, header: Union[str, None] = Header(default=None)):
#     print(body, header)

async def isAuth(req: Request):
    JWT_SECRET = "F2dN7x8HVzBWaQuEEDnhsvHXRWqAR63z"
    JWT_ALGORITHM = "HS256"
    jwtToken = req.headers.get("Authorization")
    if not jwtToken:
        return 'authError'
    if not jwtToken.startswith("Bearer "):
        return 'authError'
        # return JSONResponse(status_code=401, content=dict(msg="Authentication Error"))
    token = jwtToken.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        userId = payload['id']
        found = await userRepository.findById(userId)
        if not found:
            return 'notFound'
            # return JSONResponse(status_code=404, content=dict(msg="User not found"))
    except ExpiredSignatureError:
        return 'authError'
        #return JSONResponse(status_code=401, content=dict(msg="Authentication Error"))
    except DecodeError:
        return 'authError'
        # return JSONResponse(status_code=401, content=dict(msg="Authentication Error"))
    return dict(Authorization=f"Bearer {token}", userId = userId)

