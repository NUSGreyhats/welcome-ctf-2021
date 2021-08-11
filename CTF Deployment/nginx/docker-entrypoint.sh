#!/bin/bash

# add crontab entry to renew the letsencrypt certificate
# this cron job will run every day 11.00 P.M
echo "adding crontab"
echo "0 23 * * * certbot renew --dry-run" | crontab -

# start nginx
echo "starting nginx"
nginx