# Random Log Generator

[![Docker and Helm CI](https://github.com/example/random-log-generator/actions/workflows/docker-helm-ci.yml/badge.svg)](https://github.com/example/random-log-generator/actions/workflows/docker-helm-ci.yml)

A Python package for generating realistic log entries with configurable rates and formats, including HTTP response-like entries, and support for writing logs to a file or the console.

## Features

- Generates realistic log messages with various log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`).
- Configurable log generation rates and durations.
- Supports HTTP response-like log format.
- Option to write logs to a specified file or print to the console.
- Random rate changes and early exit probabilities for simulating real-world scenarios.
- Generates random user agents for more realistic HTTP logs.
- Collects metrics such as total logs generated, total bytes written, and average log generation rate.
- Supports custom log formats.
- Log rotation support.

## Installation

### From Source

```bash
git clone https://github.com/example/random-log-generator.git
cd random-log-generator
pip install -e .
```

### Using pip

```bash
pip install random-log-generator
```

### Using Docker

You can also run the Random Log Generator using Docker:

```bash
# Build the Docker image
docker build -t random-log-generator .

# Run the container with default configuration
docker run -v $(pwd)/logs:/app/logs random-log-generator

# Run with a custom configuration file
docker run -v $(pwd)/config.yaml:/app/config.yaml -v $(pwd)/logs:/app/logs random-log-generator --config config.yaml
```

### Using Kubernetes with Helm

If you want to deploy the Random Log Generator on a Kubernetes cluster, you can use the provided Helm chart:

```bash
# Clone the repository
git clone https://github.com/example/random-log-generator.git
cd random-log-generator

# Build and push the Docker image to your registry
docker build -t your-registry/random-log-generator:latest .
docker push your-registry/random-log-generator:latest

# Update the image repository in values.yaml
# Edit helm/random-log-generator/values.yaml and set image.repository to your-registry/random-log-generator

# Install the Helm chart
helm install my-log-generator ./helm/random-log-generator

# For more details on configuration options
helm show values ./helm/random-log-generator
```

For more information about the Helm chart, see the [Helm chart README](./helm/random-log-generator/README.md).

## Configuration

The script is configured through a YAML file. By default, it looks for `config.yaml` in the current directory, but you can specify a different path using the `-c` or `--config` option.

### Example Configuration File

```yaml
# Configuration parameters for the log generator
CONFIG:
  duration_normal: 10        # Duration of normal log generation periods in seconds
  duration_peak: 2           # Duration of peak log generation periods in seconds
  rate_normal_min: 0.0001    # Minimum log generation rate during normal periods (MB/s)
  rate_normal_max: 0.1       # Maximum log generation rate during normal periods (MB/s)
  rate_peak: 0.500           # Log generation rate during peak periods (MB/s)
  log_line_size: 100         # Approximate size of each log line in bytes
  base_exit_probability: 0.05   # Base probability to exit early from a log generation segment
  rate_change_probability: 0.1  # Probability to change the rate_max during random rate generation
  rate_change_max_percentage: 0.1  # Max percentage change when rate_max is altered
  write_to_file: true        # If true, logs will be written to a file; if false, logs will be printed to stdout
  log_file_path: 'logs.txt'  # Path to the log file
  log_rotation_enabled: true # If true, log rotation is enabled
  log_rotation_size: 50      # Size threshold for log rotation in MB
  http_format_logs: true     # If true, logs will be in HTTP log format
  stop_after_seconds: 20     # If -1, the script runs indefinitely; else, stops after specified seconds
  custom_app_names: []       # List of custom application names to include in logs
  custom_log_format: "${timestamp}, ${log_level}, ${message}"  # Custom format string for logs
  logging_level: 'INFO'      # Logging level for the script ('DEBUG', 'INFO', 'WARNING', 'ERROR')

# Log levels to use in the logs
log_levels:
  - DEBUG
  - INFO
  - WARNING
  - ERROR

# HTTP status codes and corresponding messages
http_status_codes:
  '200 OK':
    - 'API request received'
    - 'API response sent'
    # ... more messages ...
  '400 Bad Request':
    - 'Invalid user input detected'
    # ... more messages ...
  # ... more status codes ...

# User agent browsers for generating user agents
user_agent_browsers:
  - 'Chrome'
  - 'Firefox'
  # ... more browsers ...

# User agent systems for generating user agents
user_agent_systems:
  - 'Windows NT 10.0; Win64; x64'
  - 'Macintosh; Intel Mac OS X 13_4'
  # ... more systems ...
```

### Environment Variables

You can also override configuration values using environment variables. Environment variables should be prefixed with `LOG_GEN_` and be in uppercase. For example, `LOG_GEN_DURATION_NORMAL` would override `duration_normal`.

## Usage

### Command Line

```bash
# Using the default config.yaml file
random-log-generator

# Using a custom configuration file
random-log-generator -c /path/to/config.yaml

# Enable verbose output
random-log-generator -v

# Show version information
random-log-generator --version
```

### Python API

```python
from random_log_generator.config.config_loader import load_config
from random_log_generator.core.generator import main

# Load configuration
config = load_config('config.yaml')

# Run the generator
main(config)
```

## Project Structure

```
random_log_generator/
├── __init__.py
├── cli.py
├── config/
│   ├── __init__.py
│   ├── config_loader.py
│   └── validators.py
├── core/
│   ├── __init__.py
│   ├── generator.py
│   ├── rate_limiter.py
│   └── strategies.py
├── formatters/
│   ├── __init__.py
│   ├── base.py
│   ├── http.py
│   └── custom.py
├── output/
│   ├── __init__.py
│   ├── base.py
│   ├── file_output.py
│   ├── console_output.py
│   └── rotation.py
├── metrics/
│   ├── __init__.py
│   ├── collector.py
│   └── reporter.py
└── utils/
    ├── __init__.py
    ├── user_agents.py
    └── ip_generator.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## CI/CD

This project includes a GitHub Actions workflow for continuous integration:

- **Docker Build**: Automatically builds and tests the Docker image
- **Helm Lint**: Validates the Helm chart for syntax and best practices
- **Helm Test**: Deploys the chart to a test Kubernetes cluster (using kind) and verifies functionality

The workflow runs on every push to the main branch and on pull requests. You can also manually trigger it from the Actions tab in the GitHub repository.

To view the workflow status, check the Actions tab in the GitHub repository or look for the status badge at the top of this README.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
