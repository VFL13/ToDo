FROM python:3.8
ENV PYTHONUNBUFFERED 1

ADD /todos /todos/
ADD requirements.txt /todos/
WORKDIR /todos

RUN pip install -r requirements.txt