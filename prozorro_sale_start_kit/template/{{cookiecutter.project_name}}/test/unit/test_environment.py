from prozorro_sale.tools.environment import booleans
from prozorro_sale.{{cookiecutter.project_name | to_snake}}.environment import environment


class TestEnvironment:
    def test_check_default(self):
        spec = {
            {%- if cookiecutter.use_api == 'y' %}
            'API_HOST': str,
            'API_PORT': int,
            {%- endif %}
            {%- if cookiecutter.use_databridge == 'y' %}
            'DATABRIDGE_HOST': str,
            'DATABRIDGE_PORT': int,
            {%- endif %}
            {%- if (cookiecutter.use_swagger == 'y' or cookiecutter.use_swagger_yaml == 'y') %}
            'SWAGGER_DOC': booleans,
            {%- endif %}
        }
        environment.check_strict(spec, True)
