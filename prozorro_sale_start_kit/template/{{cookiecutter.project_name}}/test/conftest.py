import asyncio
import pathlib
from contextlib import contextmanager

import pytest

from prozorro_sale.{{cookiecutter.project_name | to_snake}}.databridge.main import create_databridge
from prozorro_sale.{{cookiecutter.project_name | to_snake}}.api.main import create_app

ROOT_FOLDER = pathlib.Path(__file__).parent.absolute().parent
FIXTURE_PATH = ROOT_FOLDER.joinpath('fixtures')

@pytest.fixture
async def client(aiohttp_client, loop):
    return await aiohttp_client(create_app())


@pytest.fixture
async def client_databridge(aiohttp_client, loop):
    return await aiohttp_client(create_databridge())


@contextmanager
def does_not_raise():
    yield
