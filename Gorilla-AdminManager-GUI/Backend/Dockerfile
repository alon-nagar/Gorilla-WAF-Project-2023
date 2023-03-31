FROM ubuntu:latest AS base

RUN apt-get update && apt-get install -y python3 python3-pip

COPY . .

EXPOSE 4444

RUN pip3 install flask pymongo 

CMD ["python3", "db_flask_server.py"]