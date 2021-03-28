# {{ cookiecutter.project_name }}

___

## System requirements

* make
* docker
* docker-compose
___

# Usage

## Local development

For setup local env, create py.env file:

```
{
        echo 'SERVICE_PORT=8080'
        echo 'DATABRIDGE_SERVICE_PORT=8081'
        echo 'SEARCH_URL=procedure-dev.prozori.in.ua'
        echo 'PYTHONASYNCIODEBUG=1'
        echo 'SWAGGER_DOC=1'
} > py.env
```

### Run

To start the project in development mode, run the following command:

```
make run
```

or just

```
make start
```

To stop docker containers:

```
make stop
```

To clean up docker containers (removes containers, networks, volumes, and images created by docker-compose up):

```
make remove-compose
```

or just

```
make clean
```

Shell inside the running container

```
make bash # the command can be executed only if the server is running e.g. after `make run`
```

### Help

List available `Makefile` commands

```
make help
```

### Linters

To run flake8:

```
make lint
```

All the settings for `flake8` can be customized in `.flake8` file

To run safety checks:

```
make safety
```

Check your installed dependencies for known security vulnerabilities

To find common security issues in Python code, run:

```
make bandit
```

### Type checking

Run mypy for type checking:

```
make mypy
```

Settings for `mypy` can be customized in the `mypy.ini` file.

## Software

- python3.9
