FROM ubuntu:20.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql sudo python3 python3-pip libpq-dev
RUN /etc/init.d/postgresql start \
    && sudo -u postgres psql -c "ALTER USER postgres PASSWORD '4Qgbqee5NruGGLX4c8AXF98GxTmdhrq8';" \
    && echo 'postgres:4Qgbqee5NruGGLX4c8AXF98GxTmdhrq8' | chpasswd \
    && sudo -u postgres createdb -O postgres i \
    && echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/12/main/pg_hba.conf \
    && echo "listen_addresses='*'" >> /etc/postgresql/12/main/postgresql.conf \
    && groupadd -g 1000 ctf \
    && useradd -m --no-log-init -u 1000 -g ctf ctf

WORKDIR /home/ctf/
COPY Pipfile Pipfile.lock ./
RUN python3 -m pip install pipenv \
    && sudo -u ctf pipenv sync
COPY fill_db.py server.py run.sh .env ./
COPY static/ static/
COPY html/ html/
COPY templates/ templates/
EXPOSE 8080

CMD ["./run.sh"]
