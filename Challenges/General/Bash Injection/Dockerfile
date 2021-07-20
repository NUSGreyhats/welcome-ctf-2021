# welcome-ctf pwn jail
## Based on https://github.com/redpwn/jail

# This is the source filesystem that we copy important runtime files from
FROM ubuntu:18.04 AS src
# Install additional dependencies here e.g. 32-bit runtime (lib32z1)

# This is the actual container that runs
FROM redpwn/jail:v0.0.1

# Kill each connection after 60 wall seconds (more options in https://github.com/redpwn/jail#configuration-reference)
ENV JAIL_TIME 60

# Include the bare bones of /bin from `ubuntu` (ls, cat, sh)
COPY --from=src /bin/ls /srv/bin/ls
COPY --from=src /bin/cat /srv/bin/cat
COPY --from=src /bin/sh /srv/bin/sh

# Copy the minumum required shared libraries for your binaries. Run `ldd <binary>` to find these.
# The below lines will copy libc.so.6 and ld.so from src, and are usually sufficient
COPY --from=src /lib/ /srv/lib/
COPY --from=src /lib64/ /srv/lib64/

# Copy over challenge files. Substitute ${BINARY} with the path to your binary
COPY ./get_flag.sh /srv/app/run
COPY ./hack.sh /srv/app/hack.sh
COPY ./run.sh  /srv/app/run.sh
