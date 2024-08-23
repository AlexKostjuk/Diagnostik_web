FROM python:3-slim


RUN mkdir /code
WORKDIR /code
COPY requirements_old.txt /code/

RUN pip install -r requirements_old.txt
COPY . /code/

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]