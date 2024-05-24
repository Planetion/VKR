FROM python:3.12

WORKDIR .

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:5000
