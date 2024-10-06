FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src
COPY run_app.py ./
COPY run_jobs.py ./
COPY logging_config.json ./logging_config.json

EXPOSE 5000