FROM python:3.11

WORKDIR /app

ADD . .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 8000
ENV G4F_PROXY="http://100.64.0.9:7890"

CMD ["/bin/bash","-c","uvicorn main:app --host 0.0.0.0"]
