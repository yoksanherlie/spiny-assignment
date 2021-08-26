FROM python:3.7

WORKDIR /api

ADD . /api

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]