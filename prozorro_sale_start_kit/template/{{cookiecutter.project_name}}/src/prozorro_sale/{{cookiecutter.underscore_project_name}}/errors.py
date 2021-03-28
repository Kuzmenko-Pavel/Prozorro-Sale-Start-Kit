from typing import Any

from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound, HTTPMethodNotAllowed

from prozorro_sale import tools  # type: ignore

LOG = tools.logging.get_custom_logger(__name__)


class BillingException(Exception):
    pass


ERROR_DICT = {
    HTTPNotFound: (404, '{}'),
    HTTPMethodNotAllowed: (405, '{}'),
}


@web.middleware
async def request_errors_middleware(request: web.Request, handler: Any) -> Any:
    """
    Middleware to handle common exceptions from handlers.

    For unique cases use ./utils.expects decorator.
    """
    try:
        return await handler(request)
    except tuple(ERROR_DICT.keys()) as ex:
        code, message = ERROR_DICT[type(ex)]
        LOG.info(message.format(ex))
        return web.json_response({'message': message.format(ex)}, status=code)
    except Exception as e:
        LOG.exception(f'Unknown error caught in API - {e}')
        return web.json_response({'message': 'Internal server error'}, status=500)
