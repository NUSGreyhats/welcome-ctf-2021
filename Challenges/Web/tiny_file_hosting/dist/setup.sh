#!/bin/bash
. /root/.bashrc
rm /var/www/html/upload/*
rand=`tr -dc A-Za-z0-9 </dev/urandom | head -c 17`
echo $flag > /var/www/html/upload/${rand}_flag.txt
