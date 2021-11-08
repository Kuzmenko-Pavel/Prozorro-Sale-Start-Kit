from aiohttp.web_exceptions import HTTPNotFound, HTTPMethodNotAllowed

{%- if cookiecutter.use_prozorro_tools == 'y' %}
from prozorro_sale.tools import logger
{%- else %}
import logging
{%- endif %}

{%- if cookiecutter.use_prozorro_tools == 'y' %}
LOG = logger.get_custom_logger(__name__)
{%- else %}
LOG = logging.getLogger(__name__)
{%- endif %}


class {{cookiecutter.project_name | to_camel}}Exception(Exception):
    pass


ERROR_DICT = {
    {{cookiecutter.project_name | to_camel}}Exception: (500, '{}'),
    HTTPNotFound: (404, '{}'),
    HTTPMethodNotAllowed: (405, '{}'),
}
