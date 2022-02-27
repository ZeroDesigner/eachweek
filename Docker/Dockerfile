FROM node:12
COPY Miniconda3-latest-Linux-x86_64.sh /root
COPY eachweek.yaml /root
COPY .condarc /root/
COPY ./eachweek.py /root/
RUN apt-get update && \
    apt-get install -y bash gcc make openssl wget git && \
    bash /root/Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda3 && \
    /root/miniconda3/bin/conda env create -f /root/eachweek.yaml && \
    /root/miniconda3/bin/conda clean -i -a -y
RUN mkdir /data && cd /data && \
    wget http://nginx.org/download/nginx-1.20.1.tar.gz -O /data/nginx.tar.gz &&\
    tar xzvf /data/nginx.tar.gz && cd nginx-1.20.1 && \
    ./configure --prefix=/usr/local/nginx \
    --with-http_stub_status_module && \
    make && make install && mkdir /var/log/nginx && \
    rm /usr/local/nginx/conf/nginx.conf && \
    node --version && \
    rm -rf /data/*
WORKDIR /data
RUN npm install -g -S npm --registry=https://registry.npmmirror.com && \
    npm install -g hexo-cli --registry=https://registry.npmmirror.com && \
    npm install -g hexo-wordcount --registry=https://registry.npmmirror.com && \
    npm uninstall -g hexo-renderer-marked -S && \
    npm install hexo-renderer-kramed -S -g --registry=https://registry.npmmirror.com && \
    npm uninstall hexo-generator-index -S -g && \
    npm install hexo-generator-index-pin-top -S -g --registry=https://registry.npmmirror.com && \
    npm install hexo-theme-kaze -S -g --registry=https://registry.npmmirror.com
RUN hexo init /data/Eachweek && \
    mkdir /data/Eachweek/source/_posts/nots
COPY ./nginx.conf /usr/local/nginx/conf/
EXPOSE 80
WORKDIR /data/Eachweek
COPY ./start.sh /data/Eachweek/
CMD ["bash","/data/Eachweek/start.sh"]
