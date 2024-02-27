# Beam + Flink Runner (Python Examples)


There are very few documentation on how to run Apache Beam with Flink Runner, especially for how to configure the setup. As a result, I'd like to provide an example on how we set up our infrastructure.

The example contains 2 approaches:

- Kubernetes:
  please ensure you have the official flink operator installed on your kubernetes cluster in order to run this.

- Docker Compose:
  please ensure you have docker-compose installed


In our use cases, the kubernetes is used for production, the docker-compose is for local testing/development.



# Infra Decision

1. Beam Staging Artifacts: Although Beam supports using S3 as staging artifacts. However, it seems like if we are using x-language support, the job server will not honor that settings. As a result, this example set up another PVC for job manager and task manager.

2. Minimum docker image size: In our use cases, the docker image is used in multiple areas, and thus it would be a waste of spaces if we directly put all the flink + beam dependencies in the same docker image. As a result, we are using the init container to copy the pre-built depenedencies into the current system.

3. Separate Python Harness SDK Harness to its own container.  It seems hard to control and evaluate the python usage, therefore we decide to separate the python harness so that we can just configure the container resources to control the memory assigned to python code.
