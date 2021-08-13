#!/bin/bash
# use the public IP address of the computer to accept external connections
# usage: start-php-server.sh IP PORT
IP=0.0.0.0
PORT=8000
if [ -n "$1" ]
then
  IP=$1
fi
if [ -n "$2" ]
then
  PORT=$2
fi
echo starting server on $IP:$PORT
cd serve
php -S $IP:$PORT
