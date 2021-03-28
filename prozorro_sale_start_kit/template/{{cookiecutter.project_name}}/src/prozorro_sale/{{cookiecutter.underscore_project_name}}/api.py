import os

from aiohttp import web

import prozorro_sale

SWAGGER_DOC_AVAILABLE = os.getenv('SWAGGER_DOC', False)


async def version(request: web.Request) -> web.Response:
    resp = {'api_version': prozorro_sale.version}
    if SWAGGER_DOC_AVAILABLE:
        resp['doc'] = 'If you don`t know what to do you should probably try /api/doc'
    return web.json_response(resp)


async def ping(request: web.Request) -> web.Response:
    """
    ---
    description: This end-point allows to test that service is up.
    tags:
      - Health check
    produces:
      - application/json
    responses:
      "200":
        description: successful operation. Return "pong" json
    """
    return web.json_response({'text': 'pong'})

