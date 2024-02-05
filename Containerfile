FROM python:3.10.2-slim-buster
COPY . /app
WORKDIR /app
RUN pip install .
CMD ["sandbox_exporter"]
