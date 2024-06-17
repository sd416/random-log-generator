# Log Generator Script

This script generates realistic log entries with configurable rates and formats, including HTTP response-like entries, and supports writing logs to a file or the console.

## Features

- Generates realistic log messages with various log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`).
- Configurable log generation rates and durations.
- Supports HTTP response-like log format.
- Option to write logs to a specified file or print to the console.
- Random rate changes and early exit probabilities for simulating real-world scenarios.

## Configuration

The script is configured through the following parameters. Modify the configuration parameters at the beginning of the script to customize the log generation behavior. For example:

- `duration_normal`: Duration of the normal logging period in seconds.
- `duration_peak`: Duration of the peak logging period in seconds.
- `rate_normal_min`: Minimum log generation rate during the normal period (in MB/s).
- `rate_normal_max`: Maximum log generation rate during the normal period (in MB/s).
- `rate_peak`: Log generation rate during the peak period (in MB/s).
- `log_line_size`: Average size of a log line in bytes.
- `base_exit_probability`: Base probability of exiting early during a logging segment.
- `rate_change_probability`: Probability of changing the maximum log generation rate.
- `rate_change_max_percentage`: Maximum percentage change in the log generation rate.
- `write_to_file`: Flag to indicate if logs should be written to a file (`True` or `False`).
- `log_file_path`: File path for log output (if `write_to_file` is `True`).
- `http_format_logs`: Flag to format logs in HTTP response-like format (`True` or `False`).
- `custom_app_names`: List of custom application names to be included in log messages.


## Example Configuration Parameters

```python
duration_normal = 60  # Duration of the normal logging period in seconds
duration_peak = 10  # Duration of the peak logging period in seconds
rate_normal_min = 0.0005  # Minimum log generation rate during the normal period (in MB/s)
rate_normal_max = 0.8000  # Maximum log generation rate during the normal period (in MB/s)
rate_peak = 1.5000  # Log generation rate during the peak period (in MB/s)
log_line_size = 100  # Average size of a log line in bytes
base_exit_probability = 0.10  # Base probability of exiting early during a logging segment
rate_change_probability = 0.2  # Probability of changing the maximum log generation rate
rate_change_max_percentage = 0.3  # Maximum percentage change in the log generation rate
write_to_file = True  # Flag to indicate if logs should be written to a file
log_file_path = 'logs.txt'  # File path for log output
http_format_logs = False  # Flag to format logs in HTTP response-like format
custom_app_names = ['App1', 'App2', 'App3']  # List of custom application names
```


## Usage

### Prerequisites

- Python 3.x

### Running the Script

1. Clone or download this repository.
2. Open a terminal and navigate to the directory containing the script.
3. Run the script using the following command:

```bash
python log_generator.py

```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
