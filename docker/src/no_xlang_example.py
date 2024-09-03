from __future__ import absolute_import

import argparse
import logging
import os
import sys

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


def run_pipeline():
    args = [
        "--streaming",
        "--runner=PortableRunner",
        f"--job_name={os.getenv('FLINK_JOB_NAME', 'simple-app')}",
        "--job_endpoint=localhost:8081",
    ]
    args.extend(sys.argv[1:])

    with beam.Pipeline(options=PipelineOptions(args)) as pipeline:
        print(f"Using args: {args}")
        (
            pipeline
            | beam.Create(
                [(0, "ttt"), (0, "ttt1"), (0, "ttt2"), (1, "xxx"), (1, "xxx2"), (2, "yyy")]
            )
            | beam.Map(print)
        )


if __name__ == "__main__":
    run_pipeline()
