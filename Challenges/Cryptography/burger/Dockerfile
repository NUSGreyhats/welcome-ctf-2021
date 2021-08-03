# welcome-ctf pwn jail
## Based on https://github.com/redpwn/jail
# Rudimentary per-connection python runner based on the Pwn Dockerfile template

FROM python:3 AS src

# This is the actual container that runs
FROM redpwn/jail:v0.0.1

# Kill each connection after 60 wall seconds (more options in https://github.com/redpwn/jail#configuration-reference)
ENV JAIL_TIME 1000

# Copy the entire python filesystem from src to here
COPY --from=src / /srv/
COPY server.py /srv/app/run
RUN chmod +x /srv/app/run