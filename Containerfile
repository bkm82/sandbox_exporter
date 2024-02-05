FROM python:3.10.2-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY server.py .

EXPOSE 5000

ENTRYPOINT["python", "server.py"]
