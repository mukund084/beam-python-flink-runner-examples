FROM  --platform=linux/amd64 flink:1.15.4-java8

USER root

RUN apt-get update && apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        build-essential \
        python3.9-dev \
        python3.9-venv \
        curl \
    && \
    apt-get clean

# install java SDK
COPY --from=apache/beam_java8_sdk:2.41.0 /opt/apache/beam/ /opt/apache/beam_java/

# install python SDK
COPY --from=apache/beam_python3.9_sdk:2.41.0 /opt/apache/beam/ /opt/apache/beam/

RUN mv /opt/apache/beam_java/boot /opt/apache/beam/java_boot && \
    cp -r /opt/apache/beam_java/* /opt/apache/beam/


COPY requirements.txt docker-entrypoint.sh install-flink.sh /
ENV PATH=/opt/venv/bin:/opt/flink/bin:$PATH \
    FLINK_HOME=/opt/flink \
    JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

RUN FLINK_VERSION=1.15.4 BEAM_VERSION=2.41.0 /install-flink.sh
RUN python3.9 -m venv /opt/venv && \
    /opt/venv/bin/pip install pip -U && \
    /opt/venv/bin/pip install -r /requirements.txt

COPY src/ /src
WORKDIR /src

ENTRYPOINT [ "/docker-entrypoint.sh" ]
