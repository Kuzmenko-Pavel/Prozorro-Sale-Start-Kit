{%- if cookiecutter.use_prozorro_tools == 'n' %}
import logging
{%- endif %}
from typing import AsyncGenerator

import uvloop
from aiohttp import web

import prozorro_sale  # noqa
{%- if cookiecutter.use_prozorro_tools == 'y' %}
from prozorro_sale.tools import logger
from prozorro_sale.tools.errors import catch_error_middleware
from prozorro_sale.tools.middlewares import request_id_middleware
from prozorro_sale.{{cookiecutter.project_name | to_snake}}.environment import environment, spec
{%- endif %}
from prozorro_sale.{{cookiecutter.project_name | to_snake}}.api.routes import init_routes
from prozorro_sale.{{cookiecutter.project_name | to_snake}}.errors import ERROR_DICT

{% if cookiecutter.use_prozorro_tools == 'y' %}
LOG = logger.get_custom_logger(__name__)
{%- else -%}
LOG = logging.getLogger(__name__)
{%- endif %}


async def all_start_stop_log(app: web.Application) -> AsyncGenerator[None, None]:
    LOG.info('Application is starting...')
    yield
    LOG.info('Shutting down application')


async def on_startup(app: web.Application) -> None:
    LOG.info('Load config...')


def create_databridge() -> web.Application:
    {%- if cookiecutter.use_prozorro_tools == 'y' %}
    logger.configure_logging()
    {%- endif %}
    app = web.Application(
        middlewares=[
            {%- if cookiecutter.use_prozorro_tools == 'y' %}
            request_id_middleware,
            catch_error_middleware(ERROR_DICT),
            {%- endif %}
        ]
    )
    init_routes(app)
    app.on_startup.append(on_startup)
    app.cleanup_ctx.extend([
        all_start_stop_log
    ])
    return app


def main() -> None:
    uvloop.install()
    {%- if cookiecutter.use_prozorro_tools == 'y' %}
    environment.check_strict(spec, True)
    host = environment['DATABRIDGE_HOST']
    port = environment['DATABRIDGE_PORT']
    access_log_class = logger.CustomAccessLogger
    {%- else %}
    host = None
    port = None
    access_log_class = None
    {%- endif %}
    app = create_databridge()
    web.run_app(app, host=host, port=port, access_log_class=access_log_class)


if __name__ == '__main__':
    main()
