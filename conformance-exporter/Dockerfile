# create a base image
FROM python:3.9-alpine as base
RUN python3 -m pip install --upgrade pip

# build the application requirements
FROM base as builder
COPY requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt

# add the source code (we do it last so the docker image only needs to change layers with modifications)
WORKDIR /app
ADD exporter.py /app/exporter.py

ENV PORT=8000

CMD ["python3", "-m", "exporter"]