FROM php:7.4.20-apache
COPY ./topsecret.local.conf /etc/apache2/sites-enabled/topsecret.local.conf
COPY html/ /var/www/html/
COPY cleanup-cron /etc/cron.d/cleanup-cron
RUN chown -R www-data:www-data /var/www/html && chmod ugo+w /var/www/html/tmp && chmod 600 /var/www/html/create.php /var/www/html/topsecret/index.php

RUN echo "deb http://mirror.0x.sg/debian/ buster main\ndeb http://mirror.0x.sg/debian/ buster-updates main" >> /etc/apt/sources.list
RUN apt update && apt install -y wget cron
RUN chmod 644 /etc/cron.d/cleanup-cron
RUN crontab /etc/cron.d/cleanup-cron
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb -O /tmp/wkhtmltox_0.12.5-1.buster_amd64.deb
RUN apt install -y --fix-broken /tmp/wkhtmltox_0.12.5-1.buster_amd64.deb
RUN useradd wkhtmltopdf && chown wkhtmltopdf:wkhtmltopdf `which wkhtmltopdf` && chmod u+s `which wkhtmltopdf`
CMD ["/bin/bash", "-c", "service cron start && apachectl -D FOREGROUND"]

