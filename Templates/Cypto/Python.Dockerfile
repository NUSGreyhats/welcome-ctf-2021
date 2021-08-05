# welcome-ctf pwn jail
## Based on https://github.com/redpwn/jail
# Rudimentary per-connection python runner based on the Pwn Dockerfile template

# This is the source filesystem that we copy important runtime files from
FROM python:3 AS src
# Install additional dependencies here e.g. 32-bit runtime (lib32z1)

# This is the actual container that runs
FROM redpwn/jail:v0.0.1

# Kill each connection after 60 wall seconds (more options in https://github.com/redpwn/jail#configuration-reference)
ENV JAIL_TIME 60

# Copy the entire python filesystem from src to here
COPY --from=src / /srv/
RUN rm -rf /srv/tmp

# Copy over files
COPY {files} /srv/app

# runner.sh will be the shell script that actually runs per connection
COPY runner.sh /srv/app/run