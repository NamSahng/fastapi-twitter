from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from typing import Union, List
from sqlalchemy.orm import Session

from database.db import get_db
import data.tweet as tweetRepository
from database import schemas
from middleware.auth import isAuth

router = APIRouter()


@router.get('/', response_model= List[schemas.TweetOut] , status_code=200)
async def getTweets(username : Union[str, None]=None, db : Session = Depends(get_db)):
    if username:
        data = await tweetRepository.getAllByUsername(db, username)
    else:
        data = await tweetRepository.getAll(db)
    return data


@router.get("/{id}", response_model=schemas.TweetOut, status_code=200)
async def getTweet(id: int, token : dict = Depends(isAuth), db : Session = Depends(get_db)):
    
    tweet = await tweetRepository.getById(db, id)
    if not tweet:
        raise HTTPException(status_code=404, detail=f"Tweet id({id}) not found")
    return tweet


@router.post("/", response_model=schemas.TweetOut, status_code=201)
async def createTweet(newTweet: schemas.TweetNew, token : dict = Depends(isAuth), db : Session = Depends(get_db)):
    tweet = await tweetRepository.create(db, newTweet, int(token['userId']))
    # TODO: 소켓통신 추가
    return tweet

@router.put("/{id}", response_model=schemas.TweetOut, status_code=200)
async def updateTweet(newTweet: schemas.TweetUpdate, id : int, token : dict = Depends(isAuth),  db : Session = Depends(get_db)):
    tweet = await tweetRepository.getById(db, id)
    if not tweet:
        raise HTTPException(status_code=404, detail=f"Tweet not found: {id}")    
    if tweet.userId != token['userId']:
        raise HTTPException(status_code=403)
    tweet = await tweetRepository.update(db, id, newTweet.text)    
    return tweet


@router.delete('/{id}', status_code=204)
async def deleteTweet(id : int, token : dict = Depends(isAuth),  db : Session = Depends(get_db)):
    tweet = await tweetRepository.getById(db, id)
    if not tweet:
        raise HTTPException(status_code=404, detail=f"Tweet not found: {id}")
    if tweet.userId != token['userId']:
        raise HTTPException(status_code=403)
    _ = await tweetRepository.remove(db, id)
    return Response(status_code=204)



