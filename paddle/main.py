from fastapi import FastAPI
from router import RegisterRouterList
import os, sys
import uvicorn
from dotenv import load_dotenv, find_dotenv
from router.ai import con
app = FastAPI()


for item in RegisterRouterList:
    app.include_router(item)

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)

if __name__ == "__main__":
    load_dotenv(verbose=True)
    uvicorn.run(app, loop="asyncio", host="0.0.0.0", port=8000)
