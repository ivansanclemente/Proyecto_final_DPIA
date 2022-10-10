FROM python:3.9

RUN apt-get update \
  && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential

WORKDIR /home/src

COPY inference/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY inference/src .
COPY protos/inference.proto .

ADD https://github.com/afrincon/neumonia_detector/releases/download/model/WilhemNet_86.h5 /home/src

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./inference.proto