FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install python3 -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN apt-get upgrade -y
COPY . /app
WORKDIR /app
RUN pip3 install .
RUN pip3 install -r requirements.txt
CMD ["python3", "-m", "picklr.main"]
