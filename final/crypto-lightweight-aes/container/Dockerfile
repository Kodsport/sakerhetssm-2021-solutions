FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y xinetd python3-pip
RUN python3 -m pip install pycryptodome

RUN groupadd -r ctf && useradd -r -g ctf ctf
RUN mkdir -p /home/ctf/

COPY run.sh /home/ctf/
COPY server.py /home/ctf/
COPY key /home/ctf/
COPY flag /home/ctf/
COPY xinetd_config /etc/xinetd.d/

RUN chown -R root:ctf /home/ctf/
RUN chmod -R 750 /home/ctf/

EXPOSE 50000

CMD xinetd -dontfork
