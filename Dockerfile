FROM python:3.9.14-alpine3.16

COPY ./src /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000
 
ENTRYPOINT ["uvicorn","main:app","--host","0.0.0.0"]