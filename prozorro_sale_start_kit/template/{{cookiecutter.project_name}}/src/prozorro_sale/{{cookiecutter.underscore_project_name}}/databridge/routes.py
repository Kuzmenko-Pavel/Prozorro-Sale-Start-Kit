from aiohttp import web, hdrs

from .api import version, ping, get_account_data


def init_routes(app: web.Application) -> None:
    add_route = app.router.add_route
    add_route(hdrs.METH_GET, '/api', version, name="version")
    add_route(hdrs.METH_GET, '/api/ping', ping, name="ping")
    add_route(hdrs.METH_POST, '/api/accountData/', get_account_data, name="account_data")
