FROM python:3.9-slim

COPY app/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

ADD https://github.com/just-containers/s6-overlay/releases/download/v2.2.0.1/s6-overlay-amd64-installer /tmp/
RUN \
  chmod +x /tmp/s6-overlay-amd64-installer && \
  /tmp/s6-overlay-amd64-installer / && \
  useradd -u 1970 -U -d /config -s /bin/false simon && \
  mkdir -p /config && \
  rm -rf /tmp/*

COPY app/ /app
COPY root/ /

EXPOSE 9999
VOLUME /config
ENTRYPOINT ["/init"]
