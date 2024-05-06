from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from pydantic import BaseModel
from g4f.client import Client
from g4f.Provider import OpenaiChat
from pydantic import BaseModel
import nest_asyncio
import os
from groq import Groq

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
    messages = [
        {
            "role": "user",
            "content": "接下来所有问题你必须用简体中文回答我，不需要回答英文",
        },
        {
            "role": "system",
            "content": "好的",
        },
        {
            "role": "user",
            "content": "你是谁",
        },
    ]
    await groqAI(messages, "mixtral-8x7b-32768")

    # messages = chat_request.chat
    # client = Client(provider=OpenaiChat)
    # nest_asyncio.apply()
    # response = client.chat.completions.create(
    #     api_key=chat_request.api_key,
    #     model="gpt-3.5-turbo",
    #     messages=messages,
    #     max_tokens=9999999999,
    # )
    return {"data": "1"}


class resumeParseRequest(BaseModel):
    file: UploadFile = File(...)
    api_key: str


async def groqAI(talkList: List[str], model: str):
    apikey = os.getenv("GROP_API_KEY")
    client = Groq(
        api_key=apikey,
    )
    chat_completion = client.chat.completions.create(messages=talkList, model=model)
    print(chat_completion.choices[0].message.content)
