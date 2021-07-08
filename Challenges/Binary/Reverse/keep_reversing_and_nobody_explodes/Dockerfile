FROM ubuntu:20.04

# Get python3 for emscripten and nginx for serving
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y git python3 nginx

# Download and install emscripten sdk
RUN git clone https://github.com/emscripten-core/emsdk.git 	&& \
		cd emsdk                                                && \
		git pull                                                && \
		git checkout 1.39.8                                     && \
		./emsdk install 1.39.8                                  && \
		./emsdk activate 1.39.8                                 && \
		./emsdk construct_env > /dev/null                       && \
		sed -i -e "/EM_CACHE/d" emsdk_set_env.sh

# Fix annoying python not found bug
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install pip for python libraries
RUN apt-get install -y python3-pip 

# Environment variables
ENV PATH "/emsdk:/emsdk/upstream/emscripten:/emsdk/node/12.9.1_64bit/bin:$PATH"
ENV EMSDK "/emsdk"
ENV EM_CONFIG "/root/.emscripten"
ENV EMSDK_NODE "/emsdk/node/12.9.1_64bit/bin/node"

# Use port 80 in the container
EXPOSE 80

# Copy the src folder into the container
COPY src /var/www/html
WORKDIR /var/www/html

# Compile C code to wasm
RUN emcc main.c -o main.js                    \
		-s WASM=1                                 \
		-s EXPORTED_RUNTIME_METHODS=["ccall"]     \
		-s EXPORTED_FUNCTIONS=["_malloc","_free"] \
		-s MODULARIZE                             \
		-g2                                       \
		--preload-file static/flag.txt

# Remove source code to prevent people from finding it
RUN rm main.c

# Run localhost
CMD ["nginx", "-g", "daemon off;"]