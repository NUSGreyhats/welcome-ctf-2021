#!/bin/bash

# Read three inputs to be used as positional arguments.
echo -e "Username: \c"; read user
echo -e "Password: \c"; read pass

echo

# Print the command to execute.
echo -e "[exe] -> bash -c './login.sh \"$user\" \"$pass\"'"

# Print script output.
echo -e "[out] -> \c"; bash -c "./login.sh \"$user\" \"$pass\""
