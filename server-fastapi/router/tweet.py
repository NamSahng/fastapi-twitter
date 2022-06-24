import enum
from typing import Union
import time
from fastapi import APIRouter, Response
from starlette.responses import JSONResponse
from starlette.requests import Request
from pydantic import BaseModel
router = APIRouter(prefix='/tweets')

tweets = [
    {
        "id": '1',
        "text": '잘가!',
        "createdAt": str(int(time.time() * 1000)),
        "name": 'Bob',
        "username": 'bob',
        "url": 'https://widgetwhats.com/app/uploads/2019/11/free-profile-photo-whatsapp-1.png',
    },
    {
        "id": '2',
        "text": '안녕!',
        "createdAt": str(int(time.time() * 1000)),
        "name": 'Ellie',
        "username": 'ellie',
    },
]

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


# https://fastapi.tiangolo.com/tutorial/query-params/
@router.get('/')
def get_tweets(username: Union[str, None]=None):
    if username:
        user_tweets = [tweet for tweet in tweets if tweet['username'] == username]
    else:
        user_tweets = tweets
    return JSONResponse(status_code=200, content=user_tweets)


@router.get('/{tweet_id}')
def get_tweet(tweet_id: str):
    found_tweet = [tweet for tweet in tweets if tweet['id'] == tweet_id]
    if len(found_tweet) == 0:
        return JSONResponse(status_code=404, content=dict(msg=(f'tweet id: {tweet_id} not found')))
    else:
        return JSONResponse(status_code=200, content=found_tweet)


@router.post('/')
async def create_tweet(request: Request):
    req = await request.json()

    new_tweet = {
        "id": str(int(tweets[-1]['id'])+1),
        "text": req['text'],
        "createdAt": str(int(time.time() * 1000)), # js에서 new Date()
        "name": req['name'],
        "username": req['username'],
    }
    tweets.insert(0,new_tweet)
    return JSONResponse(status_code=201, content=new_tweet)


@router.put('/{tweet_id}')
async def modify_tweet(tweet_id: str, request: Request):
    req = await request.json()
    for i, tweet in enumerate(tweets):
        if tweet['id'] == tweet_id:
            tweets[i]['text'] = req['text']
            return JSONResponse(status_code=200, content=tweet)
    return JSONResponse(status_code=404, content=dict(msg=(f'tweet id: {tweet_id} not found')))

# https://www.binaryflavor.com/fastapi-yi-204/
# https://github.com/tiangolo/fastapi/issues/717
@router.delete('/{tweet_id}', status_code=204) #response_model=Response)
def delete_tweet(tweet_id: str):
    for i, tweet in enumerate(tweets):
        if tweet['id'] == tweet_id:
            tweets.pop(i)
            return Response(status_code=204)
    # return JSONResponse(status_code=404, content=dict(msg=(f'tweet id: {tweet_id} not found')))
