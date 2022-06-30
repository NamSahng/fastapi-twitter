
from fastapi import APIRouter
from starlette.responses import JSONResponse, Response
from starlette.requests import Request
import data.tweet as tweetRepository
from middleware.auth import isAuth

router = APIRouter(prefix='/tweets')


@router.get('/')
async def getTweets(request: Request):
    isValid = await isAuth(request)    
    if len(request.query_params.keys()) != 0:
        username = request.query_params['username']
        data = await tweetRepository.getAllByUsername(username)
    else:
        data = await tweetRepository.getAll()
    return JSONResponse(status_code=200, content=data)


@router.get("/{tweetId}")
async def getTweet(request: Request, tweetId: str):
    isValid = await isAuth(request)
    if isinstance(isValid, str):
        return JSONResponse(status_code=401, content=dict(msg="Authentication Error"))
    tweet = await tweetRepository.getById(tweetId)
    return JSONResponse(status_code=200, content=tweet)


@router.post("/")
async def createTweet(request: Request):
    isValid = await isAuth(request)
    req = await request.json()
    if isinstance(isValid, str):
        return JSONResponse(status_code=401, content=dict(msg="Authentication Error"))
    newTweet = await tweetRepository.create(req['text'], isValid['userId'])
    return JSONResponse(status_code=201, content=newTweet)


@router.put("/{tweetId}")
async def updateTweet(request: Request, tweetId: int):
    req = await request.json()
    isValid = await isAuth(request)
    
    if isinstance(isValid, str):
        return JSONResponse(status_code=401, )
    tweet = await tweetRepository.getById(tweetId)
    if len(tweet) == 0:
        return JSONResponse(status_code=404, content=dict(msg=f"Tweet not found: {tweetId}"))
    if tweet[0]['userId'] != isValid['userId']:
        return JSONResponse(status_code=403, content=dict(msg="Authentication Error"))
    updated = await tweetRepository.update(tweetId, req['text'])
    return JSONResponse(status_code=200, content=updated)


@router.delete('/{tweetId}')
async def deleteTweet(tweetId: str):
    await tweetRepository.remove(tweetId)
    return Response(status_code=204)



