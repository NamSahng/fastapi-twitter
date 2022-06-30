from typing import Union


users = [
    {
        'id': '1',
        'username': 'bob',
        'password': '$2b$12$G9xf8SFq3oTEgdj7ozHQ/uhDOyeQcUEDU8tnOcvpvApuadr3nE5Vm',
        'name': 'Bob',
        'email': 'bob@gmail.com',
        'url': 'https://widgetwhats.com/app/uploads/2019/11/free-profile-photo-whatsapp-1.png',
    },
]

async def findByUsername(username: str):
    user = [user for user in users if user['username'] == username]
    if len(user) == 0:
        return None
    return user[0]


async def findById(id: str):
    user = [user for user in users if user['id'] == id]
    if len(user) == 0:
        return None
    return user[0]


async def createUser(user: dict):
    newId = str(int(users[-1]['id'])+1) if len(users) > 0 else 0
    user.update(id=newId)
    users.append(user)
    return newId

