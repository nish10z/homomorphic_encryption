FROM ubuntu:latest

ENV TZ=US/Eastern
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y sudo
RUN apt-get upgrade -y
RUN apt-get install -y git build-essential vim sudo python3 cgroup-tools
RUN apt-get -y install python3-pip
RUN pip3 install sympy

RUN adduser --disabled-password --gecos '' homomorphic
RUN adduser homomorphic sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER homomorphic
WORKDIR /home/homomorphic
RUN git clone https://github.com/nish10z/homomorphic_encryption.git