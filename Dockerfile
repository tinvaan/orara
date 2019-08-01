FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /orara
WORKDIR /orara

RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install python3-dev -y
RUN apt-get install libpq-dev -y

COPY requirements.txt /orara/
RUN pip install -r requirements.txt

COPY . /orara/

EXPOSE 80

CMD ["./run.sh"]