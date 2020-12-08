FROM ubuntu:20.04
RUN apt-get update && yes | apt-get upgrade
RUN apt-get install -y git python3-pip
RUN python3 -V
RUN python3 -m pip install --upgrade pip
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y tzdata
RUN apt-get install -y ghostscript
RUN apt-get install -y libreoffice
RUN apt-get install -y protobuf-compiler
RUN mkdir hackpions
COPY . hackpions
RUN ls hackpions -a
WORKDIR /hackpions
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
WORKDIR /hackpions/models/research
RUN protoc object_detection/protos/*.proto --python_out=.
RUN cp object_detection/packages/tf2/setup.py .
RUN python3 -m pip install .
WORKDIR /hackpions
ENV PYTHONPATH=
EXPOSE 5000
CMD [ "python3 app.py" ]
