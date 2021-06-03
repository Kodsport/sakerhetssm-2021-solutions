#!/bin/bash
sudo -u postgres /usr/lib/postgresql/12/bin/postgres -D /var/lib/postgresql/12/main -c config_file=/etc/postgresql/12/main/postgresql.conf &
sleep 10
sudo -u ctf pipenv run python3 fill_db.py
sudo -u ctf pipenv run gunicorn -b 0.0.0.0:8080 server:app
