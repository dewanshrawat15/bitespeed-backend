FROM python:3.11.4-alpine

ADD . /mysite

WORKDIR /mysite

RUN pip3 install -r requirements.txt
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
EXPOSE 8000