FROM --platform=linux/amd64 flink:1.17.2-scala_2.12-java11

USER root

# Install system packages and Python 3.12
RUN apt-get update && \
    apt-get install -y --no-install-recommends software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        python3.12 \
        python3.12-dev \
        python3.12-venv \
        curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ARG BEAM_VERSION=2.62.0
ARG FLINK_VERSION=1.17.2
ENV PATH=/opt/venv/bin:/opt/flink/bin:$PATH \
    FLINK_HOME=/opt/flink \
    JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 \
    BEAM_VERSION=${BEAM_VERSION} \
    FLINK_VERSION=${FLINK_VERSION}

# Install Beam Python SDK and Flink job server artifacts
COPY requirements.txt docker-entrypoint.sh install-flink.sh /
RUN chmod +x /install-flink.sh /docker-entrypoint.sh && \
    /install-flink.sh && \
    python3.12 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -U pip && \
    /opt/venv/bin/pip install --no-cache-dir apache-beam[gcp]==${BEAM_VERSION} && \
    /opt/venv/bin/pip install --no-cache-dir -r /requirements.txt && \
    rm /requirements.txt /install-flink.sh

COPY src/ /src
WORKDIR /src

# Expose Flink web UI and Beam job server ports for loopback execution
EXPOSE 8081 8097 8098 8099

ENTRYPOINT ["/docker-entrypoint.sh"]
