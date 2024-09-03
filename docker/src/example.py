from __future__ import absolute_import

import argparse
import logging
import os
import sys

import apache_beam as beam
from apache_beam.io.kafka import ReadFromKafka, default_io_expansion_service
from apache_beam.options.pipeline_options import PipelineOptions


def run_pipeline():
    args = [
        "--streaming",
        "--runner=PortableRunner",
        f"--job_name={os.getenv('FLINK_JOB_NAME', 'test-app')}",
    ]
    args.extend(sys.argv[1:])

    arg_parser = argparse.ArgumentParser(
        add_help=True,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    arg_parser.add_argument('--topic')
    arg_parser.add_argument('--group')
    arg_parser.add_argument('--bootstrap-server')

    options, pipeline_args = arg_parser.parse_known_args(args)

    with beam.Pipeline(options=PipelineOptions(pipeline_args)) as pipeline:
        print(f"pipeline_args: {pipeline_args}")
        topic = options.topic
        print(f"Using topic: {topic}")
        (
            pipeline
            | f"Read from kafka topic {topic}" >> ReadFromKafka(
                consumer_config={
                    "bootstrap.servers": options.bootstrap_server,
                    'auto.offset.reset': 'earliest',
                    'enable.auto.commit': 'false',
                    'group.id': options.group,
                },
                topics=topic,
                with_metadata=False,
                expansion_service=default_io_expansion_service(
                    # without the append args, it will keep trying to launch as a
                    # Docker container which is incompatible in K8s
                    append_args=[
                        '--defaultEnvironmentType=PROCESS',
                        '--defaultEnvironmentConfig={"command":"/opt/apache/beam/java_boot"}',
                        # without using the deprecated read, it will failed failrly quickly
                        '--experiments=use_deprecated_read',
                    ]
                ),
                commit_offset_in_finalize=True
            )
            | "logging" >> beam.Map(lambda x: logging.info(f"logged: {x}"))
        )


if __name__ == "__main__":
    run_pipeline()
