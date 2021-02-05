FROM python:3.8-alpine3.12

WORKDIR /projects/Economize

#INSTALL DEPENDENCIES
COPY requirements.txt .
RUN pip install -r requirements.txt

#COPY SOURCE CODE
COPY /web .

#RUN APLICATION
CMD ['python', 'manage.py', 'runserver', '0.0.0.0:5000']