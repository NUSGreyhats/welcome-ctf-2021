#!/bin/bash

# Read three inputs to be used as positional arguments.
echo "Secret #1:"
read sec1
echo "Secret #2:"
read sec2
echo "Secret #3:"
read sec3

# Hint that those inputs will be used as positional arguments in a bash script (given).
printf "\nRunning hack.sh with arguments:\n"
printf "1) $sec1\n"
printf "2) $sec2\n"
printf "3) $sec3\n\n"

printf "Executing...\n"
printf "____________________________\n\n"

bash -c "./hack.sh $sec1 $sec2 $sec3"
