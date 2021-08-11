FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY ./conf/http.conf /etc/nginx/nginx.conf

EXPOSE 80
EXPOSE 443