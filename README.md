# fastapi-twitter

Changing web framework, Express.js to FAST API. Based on this
[repo](https://github.com/NamSahng/Twitter_nodejs_pjt).


## How to run
- Server:  
```bash
$ cd server
$ make env                  # create anaconda environment
$ conda activate <new_env>  # activate anaconda environment
$ make setup                # initial setup for the project
$ python main.py            # run server
```

- Client: Node v16.13.0
```bash
$ cd client
$ npm install
$ npm start                 # run client
```

- Swagger
    - http://127.0.0.1:9999/docs
- Redoc
    - http://127.0.0.1:9999/redoc
- openapi.json
    - http://127.0.0.1:9999/openapi.json

## server/.env
```bash
DB_HOST=<DB_HOST>
DB_USER=<DB_USER>
DB_DATABASE=<DB_DATABASE>
DB_PORT=<DB_PORT>
DB_PASSWORD=<DB_PASSWORD>
JWT_SECRET=<JWT_SECRET>
JWT_EXPIRES_HOUR=<JWT_EXPIRES_HOUR>
BCRYPT_SALT_ROUNDS=<BCRYPT_SALT_ROUNDS>
CORS_ALLOW_ORIGIN=<CORS_ALLOW_ORIGIN>
```

## Todo
- set config files
- socket
- Heroku serving
- CI/CD