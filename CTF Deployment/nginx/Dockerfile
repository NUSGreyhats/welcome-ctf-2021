FROM nginx:latest

RUN rm /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
COPY ./conf/http.conf /etc/nginx/nginx.conf

EXPOSE 80 443
