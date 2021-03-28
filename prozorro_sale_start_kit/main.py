import os
from functools import partial
from pathlib import Path

import click
from PyInquirer import prompt, Separator
from pygments.token import Token
from prompt_toolkit.styles.from_dict import style_from_dict
from cookiecutter.exceptions import FailedHookException
from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter

from prozorro_sale_start_kit.utils.validator import ProjectNameValidator

parent = Path(__file__).parent

echo = partial(click.echo, err=True)

style = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 blink',
    Token.Selected: '#5F819D',
    Token.Pointer: '#FF9D00 bold',
    Token.Instruction: '#FF9D00',
    Token.Answer: '#5F819D bold',
    Token.Question: '#00FF00',
})


def show_commands(folder):
    try:
        os.chdir(f"{folder}/")  # nosec
        os.system("make help")  # nosec
    except Exception as e:
        echo(f'{e}')
        echo(click.style("\nFailed to show commands\n", fg="red", ))


def run(answers):
    template_path = str(parent / "template")
    kwargs = {
        "no_input": True,
        "extra_context": {
            "project_name": answers.get("project_name"),
            "underscore_project_name": answers.get("project_name").replace('-', '_')
        },
    }

    try:
        result = cookiecutter(template_path, **kwargs)
    except (FailedHookException, OutputDirExistsException) as exc:
        if isinstance(exc, OutputDirExistsException):
            echo(
                click.style(
                    "\n\nDirectory with such name already exists!\n", fg="red")
            )
        return

    folder = Path(result).name

    echo(click.style("\n\nSuccessfully generated!\n", fg="bright_green", ))
    echo("cd " + click.style(f"{folder}/", fg="bright_blue"))
    show_commands(folder)


def main():
    questions = [
        {
            'type': 'input',
            'qmark': '⚙',
            'name': 'project_name',
            'message': 'Enter you Project Name',
            'default': 'MyExampleProject',
            'validate': ProjectNameValidator
        },
        {
            'type': 'input',
            'qmark': '⚙',
            'name': 'gitlab_link',
            'message': 'Enter link to you GitLab Projects',
            'default': 'https://gitlab.prozorro.sale/prozorro-sale/....',
            'validate': ProjectNameValidator
        },
        {
            'type': 'checkbox',
            'qmark': '⚙',
            'message': 'Select using database',
            'name': 'database',
            'choices': [
                Separator('= The Database ='),
                {
                    'name': 'You planning to use MongoDB',
                    'value': 'use_mongo'
                },
                {
                    'name': 'You planning to use Redis',
                    'value': 'use_redis'
                }
            ],
        },
        {
            'type': 'checkbox',
            'qmark': '⚙',
            'message': 'Select planning Swagger',
            'name': 'swagger',
            'choices': [
                Separator('= The Swagger ='),
                {
                    'name': 'You planning to use Swagger',
                    'value': 'use_swagger'
                },
                {
                    'name': 'You planning to generate Swagger from Yaml',
                    'value': 'use_swagger_yaml'
                },
            ],
        },
        {
            'type': 'checkbox',
            'qmark': '⚙',
            'message': 'Select planning Project architecture component',
            'name': 'architecture',
            'choices': [
                Separator('= The Project architecture component ='),
                {
                    'name': 'You planning to use DataBridge',
                    'value': 'use_databridge'
                },
                {
                    'name': 'You planning to use Chronograph',
                    'value': 'use_chronograph'
                },
            ],
        },
        {
            'type': 'checkbox',
            'qmark': '⚙',
            'message': 'Select using prozorro packages',
            'name': 'prozorro_packages',
            'choices': [
                Separator('= The Prozorro Sale Python Packages ='),
                {
                    'name': 'You planning to use prozorro-tools',
                    'value': 'use_prozorro_tools'
                },
                {
                    'name': 'You planning to use schematics',
                    'value': 'use_schematics'
                },
                {
                    'name': 'You planning to use prozorro-auth',
                    'value': 'use_prozorro_auth'
                },
                {
                    'name': 'You planning to use prozorro-procedure',
                    'value': 'use_prozorro_procedure'
                },
                {
                    'name': 'You planning to use prozorro-mirror',
                    'value': 'use_prozorro_mirror'
                },
                {
                    'name': 'You planning to use prozorro-metrics',
                    'value': 'use_prozorro_metrics'
                },
            ],
        },
        {
            'type': 'checkbox',
            'qmark': '⚙',
            'message': 'Select using python packages',
            'name': 'python_packages',
            'choices': [
                Separator('= The Python Packages ='),
                {
                    'name': 'You planning to use uvloop',
                    'value': 'use_uvloop'
                },
                {
                    'name': 'You planning to use PyYAML',
                    'value': 'use_yaml'
                },
                {
                    'name': 'You planning to use orjson',
                    'value': 'use_orjson'
                },
                {
                    'name': 'You planning to use python-box',
                    'value': 'use_python_box'
                },
                {
                    'name': 'You planning to use trafaret',
                    'value': 'use_trafaret'
                },
                {
                    'name': 'You planning to use requests',
                    'value': 'use_requests'
                },
                {
                    'name': 'You planning to use jinja2 templates',
                    'value': 'use_aiohttp_jinja2'
                }

            ],
        },
        {
            'type': 'checkbox',
            'qmark': '⚙',
            'message': 'Select planning CI/CD',
            'name': 'ci_cd',
            'choices': [
                Separator('= The CI/CD ='),
                {
                    'name': 'You planning distribute the project as a Python package',
                    'value': 'use_setup_py'
                },
                {
                    'name': 'You planning to use Docker Compose',
                    'value': 'use_docker'
                },
                {
                    'name': 'You planning to use HELM K8s',
                    'value': 'use_helm'
                },
                {
                    'name': 'You planning to Deploy Demo in K8s',
                    'value': 'use_helm_demo'
                }
            ],
        },
        {
            'type': 'confirm',
            'qmark': '⚙',
            'name': 'use_sphinx',
            'message': 'Use Sphinx for Project Doc',
            'default': True,
        }
    ]
    try:
        answers = prompt(questions, true_color=True, patch_stdout=True, style=style)
    except AssertionError:
        echo('Run in terminal')
    else:
        print(answers)
        run(answers)


if __name__ == '__main__':
    main()
