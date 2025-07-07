FROM python

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY code/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY code/ /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

#CMD ["gunicorn", "articleInnovator.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["tail", "-f", "/dev/null"]
FROM python

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY code/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY code/ /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

#CMD ["gunicorn", "articleInnovator.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["tail", "-f", "/dev/null"]
