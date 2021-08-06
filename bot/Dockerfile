FROM python:3.7.0-stretch

RUN mkdir /app

WORKDIR /app

COPY ./ /app

RUN pip install aiogram
RUN pip install asyncio
RUN pip install requests
RUN pip install schedule

CMD python bot.py & python cron.py
