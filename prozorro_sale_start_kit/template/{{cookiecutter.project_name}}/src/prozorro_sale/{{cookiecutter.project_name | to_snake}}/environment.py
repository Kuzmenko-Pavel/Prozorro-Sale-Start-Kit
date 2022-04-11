from prozorro_sale.tools.environment import Environment, booleans

__all__ = ['environment']

spec = {
{%- if cookiecutter.use_api == 'y' %}
    'API_HOST': str,
    'API_PORT': int,
{%- endif %}
{%- if cookiecutter.use_databridge == 'y' %}
    'DATABRIDGE_HOST': str,
    'DATABRIDGE_PORT': int,
{%- endif %}
{%- if (cookiecutter.use_swagger == 'y' or  cookiecutter.use_swagger_yaml == 'y') %}
    'SWAGGER_DOC': booleans,
{%- endif %}
}
default = {
{%- if cookiecutter.use_api == 'y' %}
    'API_HOST': '0.0.0.0',
    'API_PORT': 80,
{%- endif %}
{%- if cookiecutter.use_databridge == 'y' %}
    'DATABRIDGE_HOST': '0.0.0.0',
    'DATABRIDGE_PORT': 80,
{%- endif %}
{%- if (cookiecutter.use_swagger == 'y' or  cookiecutter.use_swagger_yaml == 'y') %}
    'SWAGGER_DOC': False,
{%- endif %}
}

environment = Environment(spec=spec, default=default)
