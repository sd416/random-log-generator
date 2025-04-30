# Random Log Generator Helm Chart

This Helm chart deploys the Random Log Generator application on a Kubernetes cluster.

## Prerequisites

- Kubernetes 1.16+
- Helm 3.0+

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
# Clone the repository
git clone https://github.com/yourusername/random-log-generator.git
cd random-log-generator

# Build the Docker image
docker build -t random-log-generator:latest .

# Install the Helm chart
helm install my-release ./helm/random-log-generator
```

## Configuration

The following table lists the configurable parameters of the Random Log Generator chart and their default values.

| Parameter                | Description             | Default        |
| ------------------------ | ----------------------- | -------------- |
| `replicaCount`           | Number of replicas      | `1`            |
| `image.repository`       | Image repository        | `random-log-generator` |
| `image.tag`              | Image tag               | `latest`       |
| `image.pullPolicy`       | Image pull policy       | `IfNotPresent` |
| `config.logRate`         | Logs per second         | `10`           |
| `config.logLevels`       | Log levels to generate  | `[DEBUG, INFO, WARNING, ERROR]` |
| `config.outputType`      | Output type (file/console) | `file`      |
| `config.outputPath`      | Log file path           | `/app/logs/generated_logs.log` |
| `config.rotationSize`    | Log rotation size       | `10485760` (10MB) |
| `config.rotationCount`   | Number of rotated files | `5`            |
| `config.format`          | Log format (http/custom) | `http`        |
| `config.customFormat`    | Custom format string    | `${timestamp} ${log_level} ${message}` |

## Accessing the Logs

The logs are stored in an emptyDir volume within the pod. To access them, you can use:

```bash
# Get the pod name
POD_NAME=$(kubectl get pods -l "app.kubernetes.io/name=random-log-generator,app.kubernetes.io/instance=my-release" -o jsonpath="{.items[0].metadata.name}")

# View the logs
kubectl exec -it $POD_NAME -- cat /app/logs/generated_logs.log

# Or copy the logs to your local machine
kubectl cp $POD_NAME:/app/logs/generated_logs.log ./generated_logs.log
```

## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```bash
helm delete my-release