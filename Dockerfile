FROM ubuntu:12.04

MAINTAINER siimeon<siimeon.developer@gmail.com>

RUN apt-get update && apt-get install -y python python-django wget unzip
RUN wget https://github.com/siimeon/Kipa/archive/master.zip --no-check-certificate
RUN unzip master.zip
EXPOSE 8000:8000
WORKDIR Kipa-master/web/
CMD python manage.py runserver 0.0.0.0:8000

