FROM  ubuntu:20.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        build-essential \
        openjdk-8-jdk \
        python3-dev \
        python3.8-venv \
        curl \
    && \
    apt-get clean

# install java SDK
COPY --from=apache/beam_java8_sdk:2.41.0 /opt/apache/beam/ /opt/apache/beam_java/

# install python SDK
COPY --from=apache/beam_python3.7_sdk:2.41.0 /opt/apache/beam/ /opt/apache/beam/


COPY requirements.txt docker-entrypoint.sh install-flink.sh /
ENV PATH=/opt/venv/bin:/opt/flink/bin:$PATH \
    FLINK_HOME=/opt/flink \
    JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

RUN FLINK_VERSION=1.14.5 BEAM_VERSION=2.41.0 /install-flink.sh
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install pip -U && \
    /opt/venv/bin/pip install -r requirements.txt

COPY src/ /src
WORKDIR /src

ENTRYPOINT [ "/docker-entrypoint.sh" ]
