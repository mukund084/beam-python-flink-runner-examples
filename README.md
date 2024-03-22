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

2. Separate Python Harness SDK Harness to its own container.  It seems hard to control and evaluate the python usage, therefore we decide to separate the python harness so that we can just configure the container resources to control the memory assigned to python code.

# Docker Compose Example
1. first start the cluster:
```
docker-compose -f docker-compose.yaml up [-d]
```
2.  Trigger the app
```
python example.py \
  --topic test --group test-group --bootstrap-server host.docker.internal:9092 \
  --job_endpoint host.docker.internal:8099 \
  --artifact_endpoint host.docker.internal:8098 \
  --environment_type=EXTERNAL \
  --environment_config=host.docker.internal:50000
```
## Note
1. The example is tested in a m1 laptop. The issue for docker on mac is that I cannot use `host` and thus have to use the workaround with
`host.docker.internal` to point to the local machine port.
To ensure this work properly so that you can submit the job locally, please update `/etc/hosts` with extra line:
```
127.0.0.1 host.docker.internal
```
2. Also for M1 (or other apple chips), please ensure to enable docker settings `Use Rosetta for x86_64/amd64 emulation on Apple Silicon`



# Kubernetes Example
1. Ensure you have installed the [flink operator](https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-release-1.7/docs/try-flink-kubernetes-operator/quick-start/)

2. If you're not using Docker desktop, make sure you build the image and upload the image to the repo that your k8s can access.
```
docker build --platform linux/amd64 -t example_image:v1.0 docker/
```
3. If you've updated the docker image location, make sure you update the `image` in k8s.yaml before apply it
```
kubectl apply -f k8s.yaml
```
