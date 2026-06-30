FROM python:3.9-slim as todoList

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . /app

WORKDIR /app
EXPOSE 8000
#CMD ["gunicorn", "main:app", "-b :8000"]
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]