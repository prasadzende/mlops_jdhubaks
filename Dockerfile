FROM python:3.8-buster

ADD webapp /app/webapp
ADD prediction_service /app/prediction_service
COPY app.py params.yaml requirements.txt /app/ 

VOLUME /app

WORKDIR /app

EXPOSE 5000 

RUN pip install --no-cache-dir -r requirements.txt


CMD ["python","app.py"]
