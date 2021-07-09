#!/bin/bash

FLAG=$(./get_flag.sh)

echo Args: $#
echo --------
echo -. $0
echo 1. $1
echo 2. $2
echo 3. $3

if [ $# == 3 ]; then
    if [ $1 == "secret" ]; then
        if [ $2 == "sauce" ]; then
            if [ $3 == "yes sir" ]; then
                echo HOW?? Indeed young one, the secret sauce is: $FLAG
                exit 0
            fi
        fi
    fi
fi

echo -e "\nYou got the wrong combination of secrets."
