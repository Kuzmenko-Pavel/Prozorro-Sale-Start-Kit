from aiohttp import web

import prozorro_sale


async def version(request: web.Request) -> web.Response:
    resp = {'api_version': prozorro_sale.version}
    return web.json_response(resp)


async def ping(request: web.Request) -> web.Response:
    return web.json_response({'text': 'pong'})
