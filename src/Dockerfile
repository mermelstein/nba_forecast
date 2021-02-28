FROM python:3.8-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip==21.0

RUN pip install awscli

RUN pip install --no-cache-dir --upgrade --upgrade-strategy=eager -r requirements.txt

COPY . /app

WORKDIR /app
ENV PATH /app:$PATH

USER root

EXPOSE 8000

RUN chmod -R 777 .

CMD python -u service_run.py