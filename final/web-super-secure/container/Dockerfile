FROM php:apache

COPY index.php source.php /var/www/html/
RUN chown -R root:root /var/www/html/

COPY flag.txt /
RUN chown root:root /flag.txt
RUN chmod 644 /flag.txt
