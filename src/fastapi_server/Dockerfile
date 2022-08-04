# base image
FROM python:3.10.5-slim-buster

# add a work directory
WORKDIR /fastapi_server

# env
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /fastapi_server
RUN pip install --no-cache-dir -r requirements.txt

# copy files to the container folder
COPY . /fastapi_server

# start the server
CMD ["uvicorn", "app.fastapi_server:app", "--host", "0.0.0.0", "--port", "8001"]