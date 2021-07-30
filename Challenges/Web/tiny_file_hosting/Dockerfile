FROM php:7.4.20-apache

RUN echo "deb http://mirror.0x.sg/debian/ buster main\ndeb http://mirror.0x.sg/debian/ buster-updates main" >> /etc/apt/sources.list
RUN apt update && apt install -y cron

COPY ./setup.sh /root/setup.sh
COPY setup-cron /etc/cron.d/setup-cron
COPY app/ /var/www/html/

RUN chmod 644 /etc/cron.d/setup-cron
RUN chown www-data:www-data /var/www/html/upload
RUN crontab /etc/cron.d/setup-cron
#RUN /etc/init.d/cron start

RUN chmod +x /root/setup.sh
CMD ["/bin/bash", "-c", "service cron start && apachectl -D FOREGROUND"]

