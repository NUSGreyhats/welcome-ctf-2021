FROM php:7.4.20-apache
COPY ./topsecret.local.conf /etc/apache2/sites-enabled/topsecret.local.conf
COPY ./indocker_setup.sh /root/setup.sh

RUN echo "deb http://mirror.0x.sg/debian/ buster main" > /etc/apt/sources.list
RUN echo "deb http://mirror.0x.sg/debian/ buster-updates main" >> /etc/apt/sources.list
RUN apt update
RUN apt install -y wget
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.buster_amd64.deb -O /tmp/wkhtmltox_0.12.5-1.buster_amd64.deb
RUN apt install -y --fix-broken /tmp/wkhtmltox_0.12.5-1.buster_amd64.deb
RUN useradd wkhtmltopdf
RUN chown wkhtmltopdf:wkhtmltopdf `which wkhtmltopdf`
RUN chmod u+s `which wkhtmltopdf`
RUN chmod +x /root/setup.sh
CMD ["/bin/bash", "-c", "/root/setup.sh && apachectl -D FOREGROUND"]

