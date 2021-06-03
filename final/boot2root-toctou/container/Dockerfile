FROM python:3.9-buster

RUN apt-get update
RUN apt-get install -y sudo openssh-server

RUN adduser --disabled-password owner

RUN adduser --home /home/guest guest
RUN echo 'guest:guest' | chpasswd

WORKDIR /home/guest

COPY files/guest .
COPY files/guest /home/guest.bak
COPY files/owner /home/owner

RUN chown owner /home/owner /home/owner/*
RUN chown owner /home/guest.bak /home/guest.bak/*
RUN chown guest /home/guest /home/guest/*

RUN chmod -R 555 /home/guest.bak
RUN chmod 544 /home/owner/run.py # root = rx, others = r
RUN chmod 400 /home/owner/flag.txt

RUN chmod 777 exec edata

RUN echo 'guest ALL=(ALL) NOPASSWD: /usr/local/bin/python3 /home/owner/run.py' >> /etc/sudoers

COPY files/sshd_config /etc/ssh/sshd_config

ENTRYPOINT chown -R guest /home/guest/.ssh ; service ssh start ; sleep 10000000000000
