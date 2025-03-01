FROM python:3.10.4

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

CMD ["gunicorn", "server:app"]
