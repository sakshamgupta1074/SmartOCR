FROM python:3.8
RUN apt-get update && yes | apt-get upgrade
RUN apt-get install -y git python3-pip
RUN python3 -m pip install --upgrade pip
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
RUN python -m pip install .
WORKDIR /hackpions
RUN cp /hackpions/policy.xml /etc/ImageMagick-6/
ENV PYTHONPATH=
RUN apt-get -y install libmagickwand-dev
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
