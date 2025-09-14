FROM python:3.12-slim
WORKDIR /cxutils

COPY . .
RUN pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/simple
RUN pip install --no-cache-dir -r requirements.txt
RUN cp config.template.ini config.ini

ENV LISTEN_IP=0.0.0.0
ENV LISTEN_PORT=8000
ENV TZ='Asia/Shanghai'
EXPOSE 8000

CMD [ "python", "main.py" ]