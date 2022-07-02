from fastapi import APIRouter, Depends

from controller import tweet
from middleware.auth import isAuth

api_router = APIRouter()
api_router.include_router(tweet.router, prefix="/tweets" ,tags=["tweets"], dependencies=[Depends(isAuth)])

# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/
