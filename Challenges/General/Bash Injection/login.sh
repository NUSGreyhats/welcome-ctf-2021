#!/bin/bash

username="$1"
password="$2"

[ "$username" = "friedrice4" ] && {
    [ "$password" = "maggimee2" ] && {
        printf 'Login complete: greyhats{86sh_1n73ct10n_y6333}'
    } || {
        printf "Incorrect password."
    }
} || {
    printf "Invalid username."
}
