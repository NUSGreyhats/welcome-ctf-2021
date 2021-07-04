#!/bin/bash
chown -R www-data:www-data /var/www/html
chmod ugo+w /var/www/html/tmp
chmod 600 /var/www/html/create.php /var/www/html/topsecret/index.php
echo '127.0.0.1 topsecret.local' >> /etc/hosts
