#!/bin/bash

# Read three inputs to be used as positional arguments.
read -p "Secret #1: " sec1
read -p "Secret #2: " sec2
read -p "Secret #3: " sec3

# Hint that those inputs will be used as positional arguments in a bash script (given).
printf "\nRunning hack.sh with arguments:\n"
printf "1) $sec1\n"
printf "2) $sec2\n"
printf "3) $sec3\n\n"

printf "Executing...\n"
printf "____________________________\n\n"

bash -c "./hack.sh $sec1 $sec2 $sec3"
