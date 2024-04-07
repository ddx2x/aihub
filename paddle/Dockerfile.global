FROM python:3.11

WORKDIR /app

ADD . .
RUN pip install -r requirements.txt 
RUN pip uninstall opencv-python-headless -y && pip install opencv-python-headless

EXPOSE 8000

CMD ["/bin/bash","-c","uvicorn main:app --host 0.0.0.0"]
