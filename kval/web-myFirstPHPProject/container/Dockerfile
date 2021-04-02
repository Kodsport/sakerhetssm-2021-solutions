FROM php:apache

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y cron

COPY constants.php images.php index.php navigation.php notes.php style.css /var/www/html/
COPY entry.sh /
RUN mkdir /var/www/html/uploads_vyuncdpwhu
COPY ./uploads_vyuncdpwhu/welcome.txt /var/www/html/uploads_vyuncdpwhu
COPY ./uploads_vyuncdpwhu/welcome.txt /
RUN chown -R root:root /var/www/html/
RUN chown -R www-data:www-data /var/www/html/uploads_vyuncdpwhu
COPY flag.txt /
RUN chown root:root /flag.txt
RUN chmod 644 /flag.txt

COPY cron /etc/cron.d/cron
RUN chmod 0644 /etc/cron.d/cron
RUN crontab /etc/cron.d/cron

CMD ["/entry.sh"]
