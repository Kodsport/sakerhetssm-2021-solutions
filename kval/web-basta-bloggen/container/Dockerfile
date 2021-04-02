FROM ubuntu:20.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql golang git sudo \
    && /etc/init.d/postgresql start \
    && sudo -u postgres psql -c "ALTER USER postgres PASSWORD '8Vsrej7NjVWJqjQ2vrMDqhfBci6RJFf7';" \
    && echo 'postgres:8Vsrej7NjVWJqjQ2vrMDqhfBci6RJFf7' | chpasswd \
    && sudo -u postgres createdb -O postgres i \
    && echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/12/main/pg_hba.conf \
    && echo "listen_addresses='*'" >> /etc/postgresql/12/main/postgresql.conf \
    && groupadd -g 1000 ctf \
    && useradd -m --no-log-init -u 1000 -g ctf ctf

WORKDIR /home/ctf/
COPY run.sh go.mod go.sum database.go server.go cat_lick.gif yellow_flowers.jpg ./
RUN go build .
EXPOSE 8080

CMD ["./run.sh"]
