import asyncio
import os
from typing import AsyncGenerator

import uvloop
from aiohttp import web
from aiotask_context import task_factory

try:
    # TODO delete this after close issue
    # https://gitlab.prozorro.sale/prozorro-sale/prozorro-tools/-/issues/1
    import aiohttp_devtools  # noqa

    loop = asyncio.get_event_loop()
    loop.set_task_factory(task_factory)
except ImportError:
    pass

import prozorro_sale  # noqa
from prozorro_sale import tools  # type: ignore
from prozorro_sale.{{ cookiecutter.project_name }}.main import on_startup
from prozorro_sale.{{ cookiecutter.project_name }}.databridge.routes import init_routes
from prozorro_sale.{{ cookiecutter.project_name }}.errors import request_errors_middleware

LOG = tools.logging.get_custom_logger(__name__)


async def all_start_stop_log(app: web.Application) -> AsyncGenerator[None, None]:
    LOG.info('Application is starting...')
    yield
    LOG.info('Shutting down application')


def create_databridge() -> web.Application:
    loop = asyncio.get_event_loop()
    loop.set_task_factory(task_factory)
    tools.logging.configure_logging()
    app = web.Application(
        middlewares=[
            tools.logging.request_id_middleware,
            request_errors_middleware
        ],
        loop=loop
    )
    init_routes(app)
    app.on_startup.append(on_startup)
    app.cleanup_ctx.extend([
        all_start_stop_log
    ])
    return app


def main() -> None:
    uvloop.install()
    app = create_databridge()
    service_port = int(os.environ.get('DATABRIDGE_SERVICE_PORT', 80))
    web.run_app(app, port=service_port, access_log_class=tools.logging.CustomAccessLogger)


if __name__ == '__main__':
    main()
