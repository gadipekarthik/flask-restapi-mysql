FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# CMD [ "flask", "run" ]
CMD ["python","app.py"]
