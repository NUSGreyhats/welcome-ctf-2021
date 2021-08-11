FROM ubuntu:18.04

# install nginx
RUN apt-get update -y
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:nginx/stable
RUN apt-get update -y
RUN apt-get install -y nginx

# install certbot
RUN add-apt-repository ppa:certbot/certbot
RUN apt-get update -y
RUN apt-get install -y certbot python-certbot-nginx

# add nginx live conf
RUN rm /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
COPY ./conf/http.conf /etc/nginx/nginx.conf

# deamon mode off
RUN chown -R www-data:www-data /var/lib/nginx

# expose ports
EXPOSE 80 443

# work dir
WORKDIR /etc/nginx

# add entrypoint
ADD docker-entrypoint.sh .

# make certs dir as volume
VOLUME ["/etc/letsencrypt"]

CMD ["/etc/nginx/docker-entrypoint.sh"]