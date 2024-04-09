FROM python:3.11 as base-image
WORKDIR /app
ADD . .
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

FROM python:3.11-slim
COPY --from=base-image /usr/local/bin /usr/local/bin
COPY --from=base-image /usr/bin /usr/bin
COPY --from=base-image /usr/lib/x86_64-linux-gnu/libgomp.so.1 /usr/lib/x86_64-linux-gnu/libgomp.so.1
COPY --from=base-image /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
EXPOSE 8000
CMD ["/bin/bash","-c","uvicorn main:app --host 0.0.0.0"]
