FROM python:3.9
 
WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt
RUN apt-get update && apt-get upgrade -y && apt-get install gcc -y
RUN apt-get install google-chrome-stable -y
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 8080

USER 1000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
