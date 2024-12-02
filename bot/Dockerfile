FROM python:3.10

RUN mkdir "bot"

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

COPY ./bot_api/requirements.txt /bot/bot_api/requirements.txt

WORKDIR bot

RUN pip install -r bot_api/requirements.txt

COPY . .

CMD ["python3", "bot_api/bot.py"]