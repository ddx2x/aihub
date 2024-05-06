from fastapi import FastAPI
from router import RegisterRouterList
import os, sys
import uvicorn
from dotenv import load_dotenv, find_dotenv
import json

app = FastAPI()

for item in RegisterRouterList:
    app.include_router(item)

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
if __name__ == "__main__":
    load_dotenv(verbose=True)
    SECRET_KEY = os.getenv("REDIS_ADDRESS")
    print("SECRET_KEY", SECRET_KEY)

    uvicorn.run(app, loop="asyncio", host="0.0.0.0", port=8000)
