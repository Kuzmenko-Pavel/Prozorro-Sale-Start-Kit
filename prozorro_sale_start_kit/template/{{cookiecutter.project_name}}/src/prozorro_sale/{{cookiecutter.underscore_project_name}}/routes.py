from aiohttp import web, hdrs

from .api import version, ping


def init_routes(app: web.Application) -> None:
    add_route = app.router.add_route
    add_route(hdrs.METH_GET, '/api', version, name="version")
    add_route(hdrs.METH_GET, '/api/ping', ping, name="ping")
