#!/bin/bash
echo "installing flink=${FLINK_VERSION} BEAM=${BEAM_VERSION} …"

set -e

# enable support for S3
cd $FLINK_HOME
mkdir -p ./plugins/s3-fs-hadoop
cp ./opt/flink-s3-fs-hadoop-*.jar  ./plugins/s3-fs-hadoop
mkdir -p ./plugins/s3-fs-presto
cp ./opt/flink-s3-fs-presto-*.jar  ./plugins/s3-fs-presto

mkdir -p $FLINK_HOME/flink-web-upload
# cp $FLINK_HOME/examples/streaming/*.jar $FLINK_HOME/flink-web-upload

# install the job server which runs beam code
flink_minor_version=$(echo $FLINK_VERSION| awk -F. '{print $1"."$2}')
curl -f https://repository.apache.org/content/groups/public/org/apache/beam/beam-runners-flink-${flink_minor_version}-job-server/${BEAM_VERSION}/beam-runners-flink-${flink_minor_version}-job-server-${BEAM_VERSION}.jar -o $FLINK_HOME/flink-web-upload/beam-runner.jar

#Install the Beam expansion-service
curl -f https://repo1.maven.org/maven2/org/apache/beam/beam-sdks-java-io-expansion-service/${BEAM_VERSION}/beam-sdks-java-io-expansion-service-${BEAM_VERSION}.jar -o /opt/apache/beam_java/jars/beam-sdks-java-io-expansion-service.jar
