FROM python:3.9-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="${PYTHONPATH}:/code"

WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
