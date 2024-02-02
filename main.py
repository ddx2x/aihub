from fastapi import FastAPI
from router import RegisterRouterList
app = FastAPI()

for item in RegisterRouterList:
    app.include_router(item)
