# Create Prozorro Sale micro web service.

[![Build Status](https://travis-ci.com/Kuzmenko-Pavel/Prozorro-Sale-Start-Kit.svg?token=WYhRxCsuZNzpzJZVz7ms&branch=main)](https://travis-ci.com/Kuzmenko-Pavel/Prozorro-Sale-Start-Kit)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-green.svg)](https://github.com/Kuzmenko-Pavel/Prozorro-Sale-Start-Kit/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
[![PyPI version](https://badge.fury.io/py/prozorro-sale-start-kit.svg)](https://badge.fury.io/py/prozorro-sale-start-kit)

The tool that lets you bootstrap Prozorro Sale micro web service with best practices ready for development.

## Installation

Requires python3.9 and docker-compose

```bash
pip install prozorro-sale-start-kit
```

## Usage

```bash
PssK 
```

And answer the questions on interactive mod!


If you will create a new project called `my_project`. To start you new project run the next commands:

```bash
cd my_project

make run # start your project
```

[Here is a link to all the make commands.](https://github.com/Kuzmenko-Pavel/Prozorro-Sale-Start-Kit/wiki/Make-commands)

Then, navigate in your browser to `http://localhost:8080/`

## Salient Features

- [aiohttp](https://aiohttp.readthedocs.io/en/stable/) - the best python framework :)
- [mypy](https://mypy.readthedocs.io/en/latest/) - optional static typing
- [pytest](https://pytest.readthedocs.io/en/latest/) - unit tests
- [flake8](https://flake8.readthedocs.io/en/latest/) - linter
- [black](https://black.readthedocs.io/en/latest/) - code formatter
- [trafaret](https://trafaret.readthedocs.io/en/latest/) - data validation
- [aio devtools](https://github.com/aio-libs/aiohttp-devtools) - developer tools
- [aiohttp debug toolbar](https://github.com/aio-libs/aiohttp-debugtoolbar) - tool for debugging
- [sphinx](http://www.sphinx-doc.org/en/master/) - docs
- [docker-compose](https://docs.docker.com/compose/) - tool for defining and running multi-container Docker applications
- [py-spy](https://github.com/benfred/py-spy) - Sampling profiler for Python programs

## Options

- [ ] Project Name
  
- [ ] GitLab Projects link
  
- [ ] DataBase Support:
    - [ ] MongoDB
    - [ ] Redis
  
- [ ] Swagger Support:
    - [ ] Support YAML file
    - [ ] Support DocString
  
- [ ] Project architecture component :
    - [ ] DataBridge
    - [ ] Chronograph

- [ ] Prozorro Sale Python Packages:
    - [ ] prozorro-tools
    - [ ] schematics
    - [ ] prozorro-auth
    - [ ] prozorro-procedure
    - [ ] prozorro-mirror
    - [ ] prozorro-metrics

- [ ] Python Packages:
    - [ ] uvloop
    - [ ] PyYAML
    - [ ] orjson
    - [ ] python-box
    - [ ] trafaret
    - [ ] requests
    - [ ] jinja2
  
- [ ] CI/CD:
    - [ ] Distribute the project as a Python package
    - [ ] Docker Compose
    - [ ] HELM K8s
    - [ ] Demo in K8s
  
- [ ] Use Sphinx for Project Doc
  
## Contributing

`prozorro-sale-start-kit` is a boilerplate for Prozorro Sale community. Feel free to make any
suggestions on the issues or create a pull request. We will be very happy 😀.
See [CONTRIBUTING.md](https://github.com/Kuzmenko-Pavel/Prozorro-Sale-Start-Kit/blob/main/CONTRIBUTING.md) for
more information about how to contribute to `prozorro-sale-start-kit`.

## License

Prozorro Sale Start Kit is an open source
software <a href="https://github.com/Kuzmenko-Pavel/Prozorro-Sale-Start-Kit/blob/main/LICENSE">available under the MIT
license</a>.
