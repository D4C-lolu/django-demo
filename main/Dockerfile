FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP main.py
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
