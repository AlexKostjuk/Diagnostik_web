FROM python:3-slim


RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]