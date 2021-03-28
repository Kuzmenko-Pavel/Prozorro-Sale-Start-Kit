import asyncio
import pathlib
from contextlib import contextmanager

import pytest
from aiotask_context import task_factory

from prozorro_sale.{{ cookiecutter.underscore_project_name }}.databridge.main import create_databridge
from prozorro_sale.{{ cookiecutter.underscore_project_name }}.main import create_app

ROOT_FOLDER = pathlib.Path(__file__).parent.absolute().parent
FIXTURE_PATH = ROOT_FOLDER.joinpath('fixtures')


@pytest.fixture(autouse=True)
def aiohttp_client(aiohttp_client, loop):
    # TODO refactor this after close issue
    # https://gitlab.prozorro.sale/prozorro-sale/prozorro-tools/-/issues/1
    loop = asyncio.get_event_loop()
    loop.set_task_factory(task_factory)
    return aiohttp_client


@pytest.fixture
async def client(aiohttp_client):
    return await aiohttp_client(create_app())


@pytest.fixture
async def client_databridge(aiohttp_client):
    return await aiohttp_client(create_databridge())


@contextmanager
def does_not_raise():
    yield
