from typing import Union
from data.auth import users
from datetime import datetime
tweets = [
    {
        'id': 2,
        'text': 'bye',
        'createdAt': '2022-06-30 18:14:18',
        'userId': '1',
    },
    {
        'id': 1,
        'text': 'hi',
        'createdAt': '2022-06-30 19:14:18',
        'userId': '1',
    },
]

def getRelationTweets(tweets, users):
    userTweets = []
    for tweet in tweets:
        userId = tweet['userId']
        for user in users:
            if user['id'] == userId:
                tweet.update(username = user['username'], name = user['name'])
                userTweets.append(tweet)
    return userTweets


async def getAll(reqUsername: Union[str, None]=None):
    userTweets = getRelationTweets(tweets, users)
    if reqUsername:
        userTweets = [tweet for tweet in tweets if tweet['username'] == reqUsername]
    userTweets = sorted(userTweets, key = lambda x: datetime.strptime(x['createdAt'], "%Y-%m-%d %H:%M:%S")
                        ,reverse= True)
    return userTweets


async def getById(tweetId: int):
    userTweets = getRelationTweets(tweets, users)
    return [tweet for tweet in userTweets if tweet['id'] == tweetId]


async def getAllByUsername(username: str):
    userTweets = getRelationTweets(tweets, users)
    return [tweet for tweet in tweets if tweet['username'] == username]


async def create(text: str, userId:str):
    newId = int(tweets[0]['id'])+1 if len(tweets) > 0 else 0
    newCreatedAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    newTweet = {
        "id": newId,
        "text": text,
        "createdAt": newCreatedAt,
        "userId": userId,
    }
    tweets.insert(0, newTweet)
    userTweets = getRelationTweets(tweets, users)
    return userTweets[0]


async def update(tweetId: int, text: str):
    userTweets = getRelationTweets(tweets, users)
    for i, tweet in enumerate(userTweets):
        if tweet['id'] == tweetId:
            userTweets[i]['text'] = text
    tweets[i]['text'] = text
    return userTweets[i]


async def remove(tweetId: int):
    for i, tweet in enumerate(tweets):
        if tweet['id'] == tweetId:
            tweets.pop(i) 
