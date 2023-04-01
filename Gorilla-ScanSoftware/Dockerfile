FROM ubuntu:latest AS base

RUN apt-get update && apt-get install -y python3 python3-pip

COPY . /scan-software/ 

EXPOSE 3333

RUN pip3 install flask pymongo datetime pandas scikit-learn nltk numpy

CMD ["python3", "/scan-software/main-waf.py"]