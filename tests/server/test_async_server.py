from http import HTTPStatus
from uuid import uuid4

import pytest

from c2s_challenge.common.protocol import Response
from c2s_challenge.common.setting import SettingProvider
from c2s_challenge.server import AsyncServer, make_server_async
from c2s_challenge.server.database import DatabaseProvider
from c2s_challenge.server.event import EventRouter, EventRouterProvider


@pytest.fixture(scope="function")
def mock_async_server(
    mock_setting: SettingProvider, mock_database: DatabaseProvider
) -> AsyncServer:
    mock_router: EventRouterProvider = EventRouter(handlers={})

    server: AsyncServer = make_server_async(
        setting=mock_setting, database=mock_database, router=mock_router
    )

    return server


@pytest.mark.asyncio
async def test_event_not_found(mock_async_server: AsyncServer) -> None:
    request_raw: dict[str, any] = {"event": str(uuid4()), "data": {}}

    response: Response = await mock_async_server.process_request(request_raw)

    assert response.status == HTTPStatus.NOT_FOUND
