#!/bin/bash

if [ -n "$(ls -A keys/)" ] ; then
    echo 'Kan inte generera keys om keys/ har innehåll'
    exit
fi

cat >docker-compose.yml <<EOF
version: "2"
services:
EOF

ALLA_LAG="watevr 0xbadc0de teamjockiboi interval aguard dtttcm dataintrang freedom-dive alh3 0x2a_japanska"

PORT=2200


for LAG in $ALLA_LAG ; do
    echo "Genererar key för $LAG"
    ssh-keygen -t rsa -b 4096 -f "keys/$LAG" -C "" -N "" -q
    echo "Skapar maskin för $LAG"
    cat >>docker-compose.yml <<EOF
  b2r-$LAG:
    build: container
    volumes:
      - ./keys/$LAG.pub:/home/guest/.ssh/authorized_keys:r
    ports:
      - "$PORT:22"
    restart: on-failure
    init: true
    cpus: 0.02
EOF

    PORT=$((PORT+1))
done
