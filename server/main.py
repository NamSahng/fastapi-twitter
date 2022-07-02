
import uvicorn
from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from routes import auth, tweet



def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(auth.api_router)
    app.include_router(tweet.api_router)

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
    
