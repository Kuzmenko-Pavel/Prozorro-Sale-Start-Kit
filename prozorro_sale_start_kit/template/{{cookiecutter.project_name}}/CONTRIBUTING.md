# Contributing to {{ cookiecutter.project_name | title }}

If you open this file, it means that you want to help. Thank you for that 🤗 
Here is how to do that.

## Steps to make a pull request

1. Clone this github repo
2. Make changes
3. `make test` command must exit without errors
4. Make pull request

```bash
git clone {{ cookiecutter.gitlab_link }}
cd {{cookiecutter.gitlab_project_name}} 
pip install -r requirements/development.txt

make test

make
{%- if cookiecutter.use_api == 'y' %}
open http://localhost:8080
{%- endif %}
```

## Some possible ideas for the pull requests

 - [good first issue]({{ cookiecutter.gitlab_link }}/-/issues) - list of easy issues with description on what is have to be done
 - [documentation]({{ cookiecutter.gitlab_link }}/-/wikis/home) - documentation needs to be continuously improved 🧐
