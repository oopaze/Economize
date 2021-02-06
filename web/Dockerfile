FROM ubuntu:16.04

#MAIN APPS
RUN apt-get update
RUN apt-get -y install python-pip
RUN apt-get update
RUN pip install --upgrade pip

#SET ENVIROMENT VARIABLES
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#SET BASE PROJECT DIRECTORY
WORKDIR /projects/Economize/web

#INSTALL DEPENDENCIES
COPY requirements.txt .
RUN pip install -r requirements.txt

#COPIANDO PROJETO
COPY . .