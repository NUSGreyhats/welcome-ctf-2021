FROM php:7.4-cli

RUN apt-get update

COPY . /usr/src/app

WORKDIR /usr/src/app

EXPOSE 8000

CMD ["sh", "php-server.sh"]