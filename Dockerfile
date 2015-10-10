FROM python:2.7
ENV PYTHONUNBUFFERED 1
ADD . /
RUN pip install -r requirements.txt
EXPOSE 8000
CMD git pull && python manage.py runserver 0.0.0.0:8000
