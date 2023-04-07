FROM python:3.11

# set work directory
WORKDIR /code

COPY requirements.txt  requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .