FROM python:3.5.4@sha256:47e3dc72fcd066d926f955ff2339d7cde8e3c6d2010fb26a8832ec847fc2dfd2

WORKDIR "/tmp"

# Librdkafka v0.11.0
RUN git clone https://github.com/edenhill/librdkafka.git && \
    cd /tmp/librdkafka/ && \
    git checkout v0.11.0 && \
    ./configure && \
    make && \
    make install && \
    ldconfig

ADD requirements.txt /tmp
RUN pip install -r requirements.txt && \
    rm -rf /tmp/* && \
    mkdir -p /opt/service
ADD src /opt/service

WORKDIR /opt/service

CMD ["/bin/bash", "start.sh"]
