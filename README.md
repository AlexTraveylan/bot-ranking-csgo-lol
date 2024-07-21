# Python Template

## Description

This is a Python project that uses pytest for testing and is configured for development in Visual Studio Code. It also includes a Dockerfile for containerization.

## Project Structure

The main application code is located in the `app` directory, with the entry point in `app/main.py`. The `app` directory also contains a `core` subdirectory for core functionality and an `adapter` subdirectory for adapters.

The `tests` directory contains unit, integration, and end-to-end tests.

## Setup

### Requirements

- Python 3.10
- pip

### Installation

1. Clone the repository.
2. Install the dependencies:

```sh
pip install -r dev_requirements.txt
```

### Running the Application

To run the application:

```sh
python app/main.py
```

### Running the Tests

To run the tests:

```sh
pytest
```

## Development

This project is configured for development in Visual Studio Code with settings for the Python extension, including formatting and linting settings. The `.vscode` directory contains the configuration files.

## Docker

A Dockerfile is included for building a Docker image of the application. To build the image:

```sh
docker build -t <image-name> .
```

To run the application in a Docker container:

```sh
docker run -p 80:80 <image-name>
```

## Continuous Integration

The project includes a GitHub Actions workflow for continuous integration, which runs tests and security checks on push and pull request events to the main branch.

## Logging

The application uses Python's built-in logging module, with configuration in `app/adapter/logger/config_log.json`.

## package

To create the package, run the following command:
```bash
python setup.py sdist bdist_wheel
```

The package is available on whl file in the dist folder. To install it, run the following command:
```bash
pip install dist/<app-name>-0.1-py3-none-any.whl
```
Note : 0.1 is the version of the package, change it if needed.

## Contributing

Contributions are welcome. Please submit a pull request or create an issue to discuss the changes.

## License

[MIT](LICENSE)