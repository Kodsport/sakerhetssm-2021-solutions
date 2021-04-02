FROM ubuntu:20.04
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs npm wget gnupg ca-certificates procps libxss1 \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y google-chrome-stable \
    && groupadd -g 1000 node \
    && useradd -m --no-log-init -u 1000 -g node node

USER node
RUN mkdir -p /home/node/app
WORKDIR /home/node/app

COPY package.json package-lock.json /home/node/app/
RUN npm install
COPY src /home/node/app/src
EXPOSE 3000

CMD ["npm", "run", "start"]
