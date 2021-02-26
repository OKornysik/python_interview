FROM ubuntu:20.04

ENV PATH /usr/local/bin:$PATH

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app

RUN apt-get update && apt install -y python3
RUN apt-get install -y python3-pytest

CMD ["pytest-3", "test_apt_get_install.py"]