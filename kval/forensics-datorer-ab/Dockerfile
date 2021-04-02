FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y telnetd zip vsftpd tshark python3

COPY run.sh .
COPY vsftpd.conf /etc/vsftpd.conf
RUN mkdir -p /var/run/vsftpd/empty

RUN useradd -ms /bin/bash vd
RUN echo 'vd:sommar2021' | chpasswd 

COPY kattbilder /home/vd/kattbilder
COPY semesterbilder /home/vd/semesterbilder
COPY produktideer /home/vd/produktideer

CMD ["./run.sh"]

# How to generate chall.pcapng
# 1. run `docker-compose up --build`
# 2. run `docker-compose exec server bash`
# 2.1. run `tshark -i any -w chall.pcap` to start capturing packets
# 3. run `sudo docker inspect forensics-datorer-ab_server_1 | jq '.[0].NetworkSettings.Networks."forensics-datorer-ab_default".IPAddress'` to get the IP of the container.
# 4. connect over telnet
# 4.1. look throught all directories. `produktideer` last
# 4.2. zip all directories together using the password VXozpeHCR4oznGoiijDxCRf8LF4Go9Fc
# 4.3. exit telnet
# 5. connect over ftp
# 5.1. list the files
# 5.2. download the file x.zip
# 5.3. exit ftp
# 6. telnet in again
# 6.1. remove x.zip
# 6.2. exit telnet
# 7. stop capturing packets.
# 8. exfiltrate the pcap, filter it to only contain the relevant TCP-streams, distribute the challenge. 
