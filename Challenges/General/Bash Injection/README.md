# Challenge Details

Can you guess the username and password needed to 
unlock the flag?

# Setup Instructions

None.

# Possible Hints

You are given the command that is executed. Can
you inject a bash command?

# Key Concepts

1. Small bugs can have dire consequences.
2. User inputs can always be malicious.

# Solution

Inject a command by using this template for the
username/ password: `"; <command>; #`.

Since you know `login.sh` is executed, simply use
`"; cat login.sh; #` as either the username/ password.

# Learning Objectives

Do **NOT** use `bash -c`.

# Flag

`flag{86sh_1n73ct10n_y6333}`
