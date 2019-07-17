# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.7-stretch
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["app.py"]