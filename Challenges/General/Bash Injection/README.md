# Challenge Details

Can you guess the three secrets needed to unlock
the flag?

# Setup Instructions

Download `hack.sh`.

# Possible Hints

Why couldn't we just enter the three required
arguments? Can we, for the same reasons, perform
a command injection?

# Key Concepts

1. Small bugs can have dire consequences.
2. User inputs can always be malicious.

# Solution

Supply `word; cat get_flag.sh` as a positional
argument.

# Learning Objectives

Lack of double-quoting(s) when evaluating variables
in bash can lead to vulnerabilities like command
injections.

# Flag

`flag{86sh_1n73ct10n_y6333}`
