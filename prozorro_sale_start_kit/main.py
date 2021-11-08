import os
import sys
import argparse
import json
from functools import partial
from pathlib import Path
from urllib.parse import urlparse

import click
from PyInquirer import prompt, Separator
from pygments.token import Token
from prompt_toolkit.styles.from_dict import style_from_dict
from cookiecutter.exceptions import FailedHookException
from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter

from prozorro_sale_start_kit.utils.validator import ProjectNameValidator, ProjectLinkValidator
from prozorro_sale_start_kit.utils.patch import py_inquirer_patch


py_inquirer_patch()

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
    default_config = {}
    make_test = answers.get("make_test", False)
    template_path = parent.joinpath("template")

    kwargs = {
        "no_input": True,
        "extra_context": {
            "project_name": answers.pop("project_name", "project_new").lower(),
            "use_sphinx": "y" if answers.get("use_sphinx", True) else "n",
        },
    }
    gitlab_link = answers.pop("gitlab_link",
                              f"https://gitlab.prozorro.sale/prozorro-sale/{kwargs['extra_context']['project_name']}/")
    kwargs['extra_context']['gitlab_link'] = gitlab_link
    gitlab_project_name = urlparse(gitlab_link).path.rstrip('/').rsplit('/')[-1]
    if 'gitlab.prozorro.sale' not in gitlab_link:
        gitlab_project_name = kwargs['extra_context']['project_name']
    kwargs['extra_context']['gitlab_project_name'] = gitlab_project_name

    for value in answers.values():
        if isinstance(value, list):
            for item in value:
                kwargs["extra_context"][item] = "y"

    if any([
        kwargs["extra_context"].get('use_helm') == "y",
        kwargs["extra_context"].get('use_helm_demo') == "y",
        kwargs["extra_context"].get('use_setup_py') == "y"
    ]):
        kwargs["extra_context"]["use_docker"] = "y"

    if kwargs["extra_context"].get('use_aiohttp_jinja2') == "y":
        kwargs["extra_context"]["use_api"] = "y"

    with open(template_path.joinpath('cookiecutter.json')) as file:
        default_config = json.load(file)

    for key in default_config:
        if key in kwargs["extra_context"] or key.startswith('_'):
            continue
        kwargs["extra_context"][key] = "n" if not make_test else "y"

    try:
        result = cookiecutter(str(template_path), **kwargs)
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


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', help='test project name')
    args = parser.parse_args()
    answers = {}
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
            'default': 'https://github.com/Kuzmenko-Pavel/Prozorro-Sale-Start-Kit/',
            'validate': ProjectLinkValidator
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
                    'value': 'use_mongo',
                    'checked': False
                },
                {
                    'name': 'You planning to use Redis',
                    'value': 'use_redis',
                    'checked': False
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
                    'value': 'use_swagger',
                    'checked': True
                },
                {
                    'name': 'You planning to generate Swagger from Yaml',
                    'value': 'use_swagger_yaml',
                    'checked': False
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
                    'name': 'You planning to use API',
                    'value': 'use_api',
                    'checked': True
                },
                {
                    'name': 'You planning to use DataBridge',
                    'value': 'use_databridge',
                    'checked': False
                },
                {
                    'name': 'You planning to use Chronograph',
                    'value': 'use_chronograph',
                    'checked': False
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
                    'value': 'use_prozorro_tools',
                    'checked': True
                },
                {
                    'name': 'You planning to use schematics',
                    'value': 'use_schematics',
                    'checked': False
                },
                {
                    'name': 'You planning to use prozorro-auth',
                    'value': 'use_prozorro_auth',
                    'checked': False
                },
                {
                    'name': 'You planning to use prozorro-procedure',
                    'value': 'use_prozorro_procedure',
                    'checked': False
                },
                {
                    'name': 'You planning to use prozorro-mirror',
                    'value': 'use_prozorro_mirror',
                    'checked': False
                },
                {
                    'name': 'You planning to use prozorro-metrics',
                    'value': 'use_prozorro_metrics',
                    'checked': False
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
                    'value': 'use_uvloop',
                    'checked': True
                },
                {
                    'name': 'You planning to use python-dotenv',
                    'value': 'use_dotenv',
                    'checked': False
                },
                {
                    'name': 'You planning to use PyYAML',
                    'value': 'use_yaml',
                    'checked': False
                },
                {
                    'name': 'You planning to use ujson',
                    'value': 'use_ujson',
                    'checked': True
                },
                {
                    'name': 'You planning to use orjson',
                    'value': 'use_orjson',
                    'checked': False
                },
                {
                    'name': 'You planning to use python-box',
                    'value': 'use_python_box',
                    'checked': False
                },
                {
                    'name': 'You planning to use trafaret',
                    'value': 'use_trafaret',
                    'checked': False
                },
                {
                    'name': 'You planning to use requests',
                    'value': 'use_requests',
                    'checked': False
                },
                {
                    'name': 'You planning to use jinja2 templates',
                    'value': 'use_aiohttp_jinja2',
                    'checked': False
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
                    'value': 'use_setup_py',
                    'checked': False
                },
                {
                    'name': 'You planning to use Gitlab CI/CD',
                    'value': 'use_gitlab_ci',
                    'checked': True
                },
                {
                    'name': 'You planning to use Docker Compose',
                    'value': 'use_docker',
                    'checked': True
                },
                {
                    'name': 'You planning to use HELM K8s',
                    'value': 'use_helm',
                    'checked': True
                },
                {
                    'name': 'You planning to Deploy Demo in K8s',
                    'value': 'use_helm_demo',
                    'checked': True
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
        if project_name := args.test:
            answers['project_name'] = project_name
            answers['gitlab_link'] = f'https://gitlab.prozorro.sale/prozorro-sale/{project_name}/'
            answers['make_test'] = True
        else:
            answers.update(prompt(questions, true_color=True, patch_stdout=True, style=style))
    except AssertionError:
        echo('Run in terminal')
    else:
        if answers:
            run(answers)


if __name__ == '__main__':
    main(sys.argv[1:])
