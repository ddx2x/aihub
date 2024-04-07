from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from g4f.client import Client
from g4f.Provider import OpenaiChat
from pydantic import BaseModel
import nest_asyncio

router = APIRouter(tags=["默认路由"])

@router.get("/")
async def index():
    """
    默认访问链接
    """
    return {"code": 200, "msg": "aihub:openai!"}


class gpt35ChatRequest(BaseModel):
    chat: List[dict]
    api_key: str


@router.post("/ai/gpt35")
async def gpt35(chat_request: gpt35ChatRequest):
    messages = chat_request.chat
    client = Client(provider=OpenaiChat)
    nest_asyncio.apply()
    response = client.chat.completions.create(
        api_key=chat_request.api_key,
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=9999999999,
    )
    return {"data": response.choices[0].message.content}
