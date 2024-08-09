FROM openresty/openresty:alpine

# Install necessary packages including wget, unzip, and md5sum
RUN apk add --no-cache \
    git \
    build-base \
    openssl \
    openssl-dev \
    libgcc \
    lua5.1 \
    lua5.1-dev \
    wget \
    unzip \
    coreutils

# Install luarocks from source
RUN wget https://luarocks.org/releases/luarocks-3.8.0.tar.gz && \
    tar zxpf luarocks-3.8.0.tar.gz && \
    cd luarocks-3.8.0 && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -rf luarocks-3.8.0 luarocks-3.8.0.tar.gz

# Install lua-resty-jwt using luarocks
RUN luarocks install lua-resty-jwt

# Set the correct Lua path
ENV LUA_PATH "/usr/local/share/lua/5.1/?.lua;/usr/local/share/lua/5.1/?/init.lua;;"
ENV LUA_CPATH "/usr/local/lib/lua/5.1/?.so;/usr/local/lib/lua/5.1/?/init.so;;"

COPY nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
