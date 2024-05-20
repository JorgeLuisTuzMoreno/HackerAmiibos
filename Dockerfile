FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /hackeramiibos
WORKDIR /hackeramiibos
COPY requeriments.txt /hackeramiibos/
RUN pip install -r requeriments.txt
COPY . /hackeramiibos/
CMD python manage.py runserver 0.0.0.0:8080
