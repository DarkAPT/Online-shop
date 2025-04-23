FROM python:3.11-slim


RUN apt-get update && apt-get install -y libpq-dev
RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip --no-warn-script-location

RUN pip install -r requirements.txt --no-cache-dir --no-warn-script-location

COPY . .