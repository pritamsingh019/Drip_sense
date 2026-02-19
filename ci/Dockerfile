FROM python:3.11-slim

RUN pip install platformio
WORKDIR /project
COPY . .
RUN pio run
