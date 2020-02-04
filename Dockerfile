FROM alpine:3.11

RUN apk upgrade --update && \
    apk add --no-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ \
        uwsgi \
        uwsgi-python \
        py3-flask \
        python3 \
        nginx \
        geos && \
        rm -rf /var/cache/apk/*

RUN adduser -D -g 'www' www

COPY requirements.txt /requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r /requirements.txt && rm /requirements.txt

COPY nginx.conf /etc/nginx
COPY start.sh /
RUN chmod +x /start.sh

WORKDIR app
COPY src .

RUN mkdir /run/nginx \
    && touch /run/nginx/nginx.pid \
    && chown www:www -R . /var/log/nginx /var/lib/nginx /run/nginx \
    && setcap CAP_NET_BIND_SERVICE=+eip /usr/sbin/nginx

USER www

CMD ["/start.sh"]