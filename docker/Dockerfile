FROM  --platform=linux/amd64 flink:1.17.2-scala_2.12-java11

USER root

RUN rm -rf /var/lib/apt/lists/* && \
    apt-get update && \
    apt-get install -y --no-install-recommends software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        python3.12-dev \
        python3.12-venv \
        curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# install java SDK
COPY --from=apache/beam_java11_sdk:2.62.0 /opt/apache/beam/ /opt/apache/beam_java/

# install python SDK
COPY --from=apache/beam_python3.12_sdk:2.62.0 /opt/apache/beam/ /opt/apache/beam/

RUN mv /opt/apache/beam_java/boot /opt/apache/beam/java_boot && \
    cp -r /opt/apache/beam_java/* /opt/apache/beam/


COPY requirements.txt docker-entrypoint.sh install-flink.sh /
ENV PATH=/opt/venv/bin:/opt/flink/bin:$PATH \
    FLINK_HOME=/opt/flink \
    JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

RUN FLINK_VERSION=1.17.2 BEAM_VERSION=2.62.0 /install-flink.sh
RUN python3.12 -m venv /opt/venv && \
    /opt/venv/bin/pip install pip -U && \
    /opt/venv/bin/pip install -r /requirements.txt

COPY src/ /src
WORKDIR /src

ENTRYPOINT [ "/docker-entrypoint.sh" ]
