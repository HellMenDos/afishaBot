FROM python:3.6
RUN mkdir /admin
COPY ./ /admin
WORKDIR /admin
RUN pip install -r requirements.txt --no-cache-dir

CMD python manage.py runserver 0.0.0.0:8000