from fastapi import APIRouter, Depends

from controller import auth


api_router = APIRouter()
# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/
api_router.include_router(auth.router, prefix="/auth" ,tags=["auth"])


