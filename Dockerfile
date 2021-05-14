FROM python:3.8.3-slim

EXPOSE 5000/tcp

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

WORKDIR /app/src

CMD [ "python", "app.py"]