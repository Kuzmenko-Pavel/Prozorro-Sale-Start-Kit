import shutil
import os

from prozorro_sale_start_kit.constants import EXTENSIONS


def remove_dirs_and_files(file_type) -> None:
    if extension := EXTENSIONS.get(file_type):
        for dir_name in extension.get('TEMPLATE_DIRS', []):
            shutil.rmtree(f'{{cookiecutter.project_name}}/{dir_name}')

        for file_name in extension.get('TEMPLATE_FILES', []):
            os.remove(f'{{cookiecutter.project_name}}/{file_name}')


def main() -> None:
    without_swagger_yaml = "{{ cookiecutter.use_swagger_yaml | lower }}" == "n"
    without_databridge = "{{ cookiecutter.use_databridge | lower }}" == "n"
    without_chronograph = "{{ cookiecutter.use_chronograph | lower }}" == "n"
    without_setup_py = "{{ cookiecutter.use_setup_py | lower }}" == "n"
    without_docker = "{{ cookiecutter.use_docker | lower }}" == 'n'
    without_helm = "{{ cookiecutter.use_helm | lower }}" == 'n'
    without_helm_demo = "{{ cookiecutter.use_helm_demo | lower }}" == 'n'
    without_sphinx = "{{ cookiecutter.use_sphinx | lower }}" == 'n'

    if without_swagger_yaml:
        remove_dirs_and_files('swagger_yaml')

    if without_databridge:
        remove_dirs_and_files('databridge')

    if without_chronograph:
        remove_dirs_and_files('chronograph')

    if without_setup_py:
        remove_dirs_and_files('setup_py')

    if without_docker:
        remove_dirs_and_files('docker')

    if without_helm:
        remove_dirs_and_files('helm')

    if without_helm_demo:
        remove_dirs_and_files('helm_demo')

    if without_sphinx:
        remove_dirs_and_files('sphinx')


if __name__ == "__main__":
    main()
