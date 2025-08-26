from __future__ import absolute_import

import os
import re
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
        lines = pipeline | beam.Create(
            [
                "to be or not to be",
                "that is the question",
            ]
        )
        (
            lines
            | "Split" >> beam.FlatMap(lambda line: re.findall(r"[A-Za-z']+", line.lower()))
            | "PairWithOne" >> beam.Map(lambda word: (word, 1))
            | "GroupAndSum" >> beam.CombinePerKey(sum)
            | "Format" >> beam.Map(lambda kv: f"{kv[0]}: {kv[1]}")
            | "Print" >> beam.Map(print)
        )


if __name__ == "__main__":
    run_pipeline()
