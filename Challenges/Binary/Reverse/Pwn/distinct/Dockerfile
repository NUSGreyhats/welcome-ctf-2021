FROM ubuntu:16.04

EXPOSE 9999

# In case we need the specific Xinetd from Eadom
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.ustc.edu.cn/g" /etc/apt/sources.list

RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get install -y xinetd dos2unix

# For 32-bit support
# RUN apt-get install -y lib32z1

RUN useradd -m ctf

WORKDIR /home/ctf

# Copy over lib files
RUN cp -R /lib* /home/ctf && \
    cp -R /usr/lib* /home/ctf

# Copy over /dev/{null,zero,random,urandom}
RUN mkdir /home/ctf/dev && \
    mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/*

# Copy over the bare-minimum of binaries
RUN mkdir /home/ctf/bin && \
    cp /bin/sh /home/ctf/bin && \
    cp /bin/ls /home/ctf/bin && \
    cp /bin/cat /home/ctf/bin

# Setup xinetd 
RUN rm /etc/xinetd.d/*
COPY ./infra/ctf.xinetd /etc/xinetd.d/ctf
# xinetd hates dos characters in its configs
RUN dos2unix /etc/xinetd.d/ctf
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

# Copy over challenge files
COPY ./flag.txt /home/ctf
COPY ./dist/distinct.o /home/ctf

# Set perms
RUN chown -R root:ctf /home/ctf && \
    chmod -R 550 /home/ctf && \
    chmod -R 750 /home/ctf/dev && \
    chmod 444 /home/ctf/flag.txt

# Run start.sh
COPY ./infra/start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]