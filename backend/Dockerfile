# pull official base image
FROM python:3.8.1-slim-buster

# create directory for the app / app user
RUN mkdir -p /home/app

# set work directory for copying files
WORKDIR /home/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat sqlite3

# install dependencies (doesn't change often)
RUN pip install --upgrade pip
COPY ./requirements.txt /home/app/requirements.txt
RUN pip install -r requirements.txt

# copy rest of project
COPY . /home/app/

# run entrypoint.sh
ENTRYPOINT ["/home/app/entrypoint.sh"]
