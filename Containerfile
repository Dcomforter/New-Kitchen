FROM python:3.12

ENV PYTHONUNBUFFERED 1

WORKDIR /mykitchen

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


