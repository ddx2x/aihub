from fastapi import FastAPI
from router import RegisterRouterList
import os,sys
import uvicorn

import nest_asyncio
nest_asyncio.apply()

app = FastAPI()

for item in RegisterRouterList:
    app.include_router(item)

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)