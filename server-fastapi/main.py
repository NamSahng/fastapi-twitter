
import uvicorn
from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from routes import tweet, auth

def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(auth.router)
    app.include_router(tweet.router)

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
    
