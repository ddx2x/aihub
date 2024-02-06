from fastapi import APIRouter
from fastapi import File,UploadFile,Form
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
import os, uuid


router = APIRouter(tags=["默认路由"])

@router.get("/")
async def index():
    """
    默认访问链接
    """
    return {
        "code": 200,
        "msg": "Hello AI!"
    }


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
    save_results = ''


    for _, img in enumerate(ocr_imgs):
            dt_boxes, rec_res, time_dict = text_sys(img)

            res = ''
            for i in range(len(dt_boxes)):
                if rec_res[i][1]>=0.9:
                    res += rec_res[i][0]

            save_results += res

    return {"data": save_results}

