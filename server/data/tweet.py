from typing import Union
from sqlalchemy.orm import Session
from database.models import Tweets, Users
from database import schemas


ORDERBY = Tweets.createdAt.desc()
tweetForm = [Tweets.id, Tweets.text, Tweets.createdAt, Tweets.userId, Users.name, Users.username, Users.url]


async def getAll(db: Session):
    return db.query(*tweetForm)\
                .join(Users)\
                .order_by(ORDERBY)\
                .all()

async def getAllByUsername(db : Session, username: str):
    return db.query(*tweetForm)\
                .join(Users)\
                .order_by(ORDERBY)\
                .filter(Users.username==username)\
                .all()


async def getById(db : Session, id: int):
    return db.query(*tweetForm)\
                .join(Users)\
                .filter(Tweets.id==id)\
                .first()


async def create(db : Session, tweet : schemas.TweetNew, userId : int):
    db_tweet = Tweets(text = tweet.text, userId=userId)
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return await getById(db, db_tweet.id)
    
async def update(db : Session, tweetId : int, newText : str):
    db_tweet = db.query(Tweets).filter(Tweets.id == tweetId).first()
    db_tweet.text = newText
    db.commit()
    return await getById(db, tweetId)

async def remove(db : Session, tweetId: int):
    db_tweet = db.query(Tweets).filter(Tweets.id == tweetId).delete()
    db.commit()
    return db_tweet
