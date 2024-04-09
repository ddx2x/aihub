FROM python:3.11

WORKDIR /app

ADD . .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 8000

CMD ["/bin/bash","-c","uvicorn main:app --host 0.0.0.0"]
