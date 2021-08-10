FROM python:3.7-slim-buster
WORKDIR /opt/CTFd
RUN mkdir -p /opt/CTFd /var/log/CTFd /var/uploads

# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libffi-dev \
        libssl-dev \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/CTFd/

RUN pip install -r requirements.txt --no-cache-dir

COPY . /opt/CTFd

# hadolint ignore=SC2086
RUN for d in CTFd/plugins/*; do \
        if [ -f "$d/requirements.txt" ]; then \
            pip install -r $d/requirements.txt --no-cache-dir; \
        fi; \
    done;

RUN adduser \
    --disabled-login \
    -u 1001 \
    --gecos "" \
    --shell /bin/bash \
    ctfd
RUN chmod +x /opt/CTFd/docker-entrypoint.sh \
    && chown -R 1001:1001 /opt/CTFd /var/log/CTFd /var/uploads


# install certbot and nginx, configuration
RUN apt-get update -y
RUN apt-get install -y nginx
RUN apt-get install -y certbot python-certbot-nginx

RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
RUN chown -R www-data:www-data /var/lib/nginx

EXPOSE 80 443

# add nginx staging conf
ADD /etc/nginx/sites-available/welcomectf.tk

# create symlinks
RUN ln -s /etc/nginx/sites-available/welcomectf.tk /etc/nginx/sites-enabled/welcomectf.tk

# work dir
WORKDIR /etc/nginx

VOLUME ["/etc/letsencrypt"]

USER 1001
EXPOSE 8000 
ENTRYPOINT ["/opt/CTFd/docker-entrypoint.sh"]
