FROM python:3.10

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

COPY ./bot_api/requirements.txt /bot/bot_api/requirements.txt

WORKDIR bot 
# Директория создается автоматом 

RUN pip install -r bot_api/requirements.txt

