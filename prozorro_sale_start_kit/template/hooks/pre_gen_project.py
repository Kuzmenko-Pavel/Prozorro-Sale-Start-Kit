import sys

import click

from prozorro_sale_start_kit.utils.validator import name_type, name_underscore_type


def validate_project_name(project_name: str) -> None:
    try:
        name_type(project_name)
    except NameError as exc:
        click.echo(str(exc), err=True)
        sys.exit(1)


def validate_underscore_project_name(underscore_project_name: str) -> None:
    try:
        name_underscore_type(underscore_project_name)
    except NameError as exc:
        click.echo(str(exc), err=True)
        sys.exit(1)


def main() -> None:
    validate_project_name('{{ cookiecutter.project_name }}')
    validate_underscore_project_name('{{ cookiecutter.underscore_project_name }}')


if __name__ == '__main__':
    main()
