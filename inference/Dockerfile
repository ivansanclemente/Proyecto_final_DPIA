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

RUN curl "https://www.dropbox.com/s/yx6n606i7cfcvoz/WilhemNet_86.h5?dl=1" -L -o WilhemNet_86.h5

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./inference.proto