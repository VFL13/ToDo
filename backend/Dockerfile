FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

ADD /todos /todo/
ADD requirements.txt /todo/
WORKDIR /todo

RUN pip install -r requirements.txt