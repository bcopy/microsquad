FROM python:3.8-slim

ADD src/main/python /app

RUN cd /app && pip install -r requirements.txt

WORKDIR /app

CMD ["python", "-m","microsquad.gateway.mqtt"]