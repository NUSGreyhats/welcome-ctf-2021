FROM ubuntu:latest
RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install software-properties-common -y
RUN LC_ALL=C.UTF-8 add-apt-repository ppa:ondrej/php -y
RUN apt-get update -y
RUN apt-get install -y tzdata
RUN apt-get install php7.0 -y
RUN a2enmod php7.0 && service apache2 restart

# Remove example files
RUN rm -rfd /var/www/example.com
RUN rm /var/www/html/index.html

# Add our source files
RUN echo "<VirtualHost *:80>\r\nServerName SomeServer\r\nDocumentRoot /var/www/html\r\n</VirtualHost>" > /etc/apache2/sites-enabled/000-default.conf
COPY ./serve /var/www/html

# Copy and define entrypoint
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 80
