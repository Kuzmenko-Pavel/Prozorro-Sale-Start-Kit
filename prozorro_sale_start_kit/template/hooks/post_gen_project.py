import shutil
import os

from prozorro_sale_start_kit.template.hooks.constants import EXTENSIONS


def remove_dirs_and_files(file_type) -> None:
    data_format = {
        'underscore_project_name': '{{cookiecutter.project_name | to_snake}}'
    }
    if extension := EXTENSIONS.get(file_type):
        for dir_name in extension.get('TEMPLATE_DIRS', []):
            print(dir_name)
            shutil.rmtree(dir_name.format(**data_format), ignore_errors=True)

        for file_name in extension.get('TEMPLATE_FILES', []):
            try:
                os.remove(file_name.format(**data_format))
            except OSError:
                pass


def main() -> None:
    elements = [
        ('mongo', "{{ cookiecutter.use_mongo | lower }}" == "n"),
        ('redis', "{{ cookiecutter.use_redis | lower }}" == "n"),
        ('swagger', "{{ cookiecutter.use_swagger | lower }}" == "n"),
        ('swagger_yaml', "{{ cookiecutter.use_swagger_yaml | lower }}" == "n"),
        ('api', "{{ cookiecutter.use_api | lower }}" == "n"),
        ('databridge', "{{ cookiecutter.use_databridge | lower }}" == "n"),
        ('chronograph', "{{ cookiecutter.use_chronograph | lower }}" == "n"),
        ('prozorro_tools', "{{ cookiecutter.use_prozorro_tools | lower }}" == "n"),
        ('schematics', "{{ cookiecutter.use_schematics | lower }}" == "n"),
        ('prozorro_auth', "{{ cookiecutter.use_prozorro_auth | lower }}" == "n"),
        ('prozorro_procedure', "{{ cookiecutter.use_prozorro_procedure | lower }}" == "n"),
        ('prozorro_mirror', "{{ cookiecutter.use_prozorro_mirror | lower }}" == "n"),
        ('prozorro_metrics', "{{ cookiecutter.use_prozorro_metrics | lower }}" == "n"),
        ('uvloop', "{{ cookiecutter.use_uvloop | lower }}" == "n"),
        ('yaml', "{{ cookiecutter.use_yaml | lower }}" == "n"),
        ('orjson', "{{ cookiecutter.use_orjson | lower }}" == "n"),
        ('python_box', "{{ cookiecutter.use_python_box | lower }}" == "n"),
        ('trafaret', "{{ cookiecutter.use_trafaret | lower }}" == "n"),
        ('requests', "{{ cookiecutter.use_requests | lower }}" == "n"),
        ('aiohttp_jinja2', "{{ cookiecutter.use_aiohttp_jinja2 | lower }}" == "n"),
        ('setup_py', "{{ cookiecutter.use_setup_py | lower }}" == "n"),
        ('gitlab_ci', "{{ cookiecutter.use_gitlab_ci | lower }}" == "n"),
        ('docker', "{{ cookiecutter.use_docker | lower }}" == "n"),
        ('helm', "{{ cookiecutter.use_helm | lower }}" == "n"),
        ('helm_demo', "{{ cookiecutter.use_helm_demo | lower }}" == "n"),
        ('sphinx', "{{ cookiecutter.use_sphinx | lower }}" == "n"),
    ]
    for name, removed in elements:
        if removed:
            remove_dirs_and_files(name)


if __name__ == "__main__":
    main()
