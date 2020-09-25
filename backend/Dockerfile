FROM python:3.8
ENV PYTHONUNBUFFERED 1

ADD /todo /todo/
ADD requirements.txt /todo/
WORKDIR /todo

RUN pip install -r requirements.txt