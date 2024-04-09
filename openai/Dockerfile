FROM python:3.11
WORKDIR /app
ADD . .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

EXPOSE 8000
CMD ["/bin/bash","-c","uvicorn main:app --loop asyncio --host 0.0.0.0"]
