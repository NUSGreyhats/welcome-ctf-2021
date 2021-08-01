# welcome-ctf pwn jail
## Based on https://github.com/redpwn/jail

# This is the source filesystem that we copy important runtime files from
FROM ubuntu:18.04 AS src
# Install additional dependencies here e.g. 32-bit runtime (lib32z1)

# This is the actual container that runs
FROM redpwn/jail:v0.0.1

# Kill each connection after 60 wall seconds (more options in https://github.com/redpwn/jail#configuration-reference)
ENV JAIL_TIME 60

# Since this is a bash challenge, we include all the bash programs here
COPY --from=src /bin/* /srv/bin/

# Copy the minumum required shared libraries for your binaries. Run `ldd <binary>` to find these.
# The below lines will copy libc.so.6 and ld.so from src, and are usually sufficient
COPY --from=src /lib/ /srv/lib/
COPY --from=src /lib64/ /srv/lib64/

# Copy over challenge files. Substitute ${BINARY} with the path to your binary
COPY ./login.sh /srv/app/login.sh
COPY ./run.sh  /srv/app/run
