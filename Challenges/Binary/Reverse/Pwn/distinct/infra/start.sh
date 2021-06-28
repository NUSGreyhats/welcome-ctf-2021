#!/bin/sh

# Test for configuration errors
# script -c "/usr/sbin/xinetd -d -dontfork";

# Normal start
/etc/init.d/xinetd start;

sleep infinity;