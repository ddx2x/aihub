from fastapi import APIRouter
from fastapi import File, UploadFile, Form
import fitz
from PIL import Image
import cv2
import numpy as np
from typing import List, Optional
import base64
import io
import pad.ocr.utility as utility
import pad.ocr.predict_system as predict_system
from router.config import Config
from router.util import idPhoto
import os, uuid
from pydantic import BaseModel, Field
from g4f.client import Client
from g4f.Provider import OpenaiChat
from pydantic import BaseModel
import g4f
import nest_asyncio


router = APIRouter(tags=["默认路由"])


@router.get("/")
async def index():
    """
    默认访问链接
    """
    return {"code": 200, "msg": "Hello AI!"}


@router.post("/ai/ocr")
async def ai_ocr(base64_imgs: Optional[List[str]] = None, pdf: UploadFile = File(None)):
    ocr_imgs = []
    if pdf:
        filename = f"{uuid.uuid4()}_{pdf.filename}"
        pdf_data = await pdf.read()
        with open(filename, "wb") as temp_pdf_file:
            temp_pdf_file.write(pdf_data)
        with fitz.open(filename) as temp_pdf:
            for pg in range(0, temp_pdf.page_count):
                page = temp_pdf[pg]
                mat = fitz.Matrix(2, 2)
                pm = page.get_pixmap(matrix=mat, alpha=False)

                # if width or height > 2000 pixels, don't enlarge the image
                if pm.width > 2000 or pm.height > 2000:
                    pm = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)

                img = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
                img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                ocr_imgs.append(img)
        os.remove(filename)

    if base64_imgs:
        for img_b64 in base64_imgs:
            # 将base64字符串解码为二进制数据
            img_data = base64.b64decode(img_b64)
            # 使用BytesIO创建一个流，PIL.Image.open来从这个流中读取图片
            img = Image.open(io.BytesIO(img_data))
            ocr_imgs.append(img)

    config = Config()
    text_sys = predict_system.TextSystem(config)
    save_results = ""

    for _, img in enumerate(ocr_imgs):
        dt_boxes, rec_res, time_dict = text_sys(img)

        res = ""
        for i in range(len(dt_boxes)):
            if rec_res[i][1] >= 0.9:
                res += rec_res[i][0]

        save_results += res

    return {"data": save_results}


class ChangeBgColorRequest(BaseModel):
    base64_img: Optional[str] = Field(None, description="The base64 encoded image")
    color: Optional[str] = Field(None, description="The color to use as background")


@router.post("/ai/change_bg_color")
async def ai_ocr(data: ChangeBgColorRequest):

    if data.base64_img is None or data.color is None:
        raise HTTPException(
            status_code=400, detail="Missing base64_img or color in the request"
        )
    img_data = base64.b64decode(data.base64_img)
    img = Image.open(io.BytesIO(img_data))

    img_name = f"{uuid.uuid4()}-img.png"
    bg_name = f"{uuid.uuid4()}-bg.png"

    img.save(img_name)

    # 去掉背景颜色
    os.system(f'backgroundremover -i "{img_name}" -o "{bg_name}"')
    # 加上背景颜色
    no_bg_image = Image.open(bg_name).convert("RGBA")
    x, y = no_bg_image.size
    new_image = Image.new("RGBA", no_bg_image.size, color=data.color)
    new_image.paste(no_bg_image, (0, 0, x, y), no_bg_image)

    buffered = io.BytesIO()
    new_image.save(buffered, format="PNG")
    buffered.seek(0)

    # Encode the modified image to base64
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    for file in [img_name, bg_name]:
        os.remove(file)

    return {"data": img_base64}


class GetIdCardImg(BaseModel):
    base64_img: Optional[str] = Field(None, description="The base64 encoded image")
    inch_choice: Optional[int] = Field(None, description="ince choice")


@router.post("/ai/get_id_card_img")
async def get_id_card_img(data: GetIdCardImg):
    img_data = base64.b64decode(data.base64_img)
    img = Image.open(io.BytesIO(img_data))
    new_img = idPhoto(img, data.inch_choice)

    buffered = io.BytesIO()
    new_img.save(buffered, format="PNG")
    buffered.seek(0)

    # Encode the modified image to base64
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"data": img_base64}


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
