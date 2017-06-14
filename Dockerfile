FROM python:3.6.1

WORKDIR /usr/src/app
RUN export DATABASE_URL=sqlite:////usr/src/app/db.sqlite3

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py migrate --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]

EXPOSE 80
