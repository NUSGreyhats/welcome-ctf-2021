#!/bin/bash
rm /var/www/html/upload/*
rand=`tr -dc A-Za-z0-9 </dev/urandom | head -c 13`
echo "greyhats{h0vv_d1d_y0u_byp455_17?!?!}" > /var/www/html/upload/${rand}_flag.txt
