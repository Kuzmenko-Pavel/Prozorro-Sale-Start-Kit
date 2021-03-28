import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'requirements/requirements.txt')) as f:
    requirements = ''
    for line in f.readlines():
        if not line.startswith('-i') or not line.startswith('-r'):
            requirements += line

setup(
    name='{{ cookiecutter.project_name }}',
    version_format='{tag}',
    setup_requires=['setuptools-git-version'],
    description='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=requirements,
    package_data={'': ['*.yml']},
    include_package_data=True
)
