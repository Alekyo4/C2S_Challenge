from c2s_challenge.common.protocol.model import RequestEvent
from c2s_challenge.common.setting import Setting, SettingProvider

from .agent import AgentAIProvider, GeminiAgentAI
from .database import Database, DatabaseProvider
from .event import EventRouter, EventRouterProvider
from .event.handler import VehicleChatHandler, VehicleSearchHandler
from .provider import AsyncServerProvider, SyncServerProvider


def make_server_sync(
    setting: SettingProvider | None = None,
    database: DatabaseProvider | None = None,
    agent_ai: AgentAIProvider | None = None,
) -> SyncServerProvider:
    raise NotImplementedError()


def make_server_async(
    setting: SettingProvider | None = None,
    database: DatabaseProvider | None = None,
    agent_ai: AgentAIProvider | None = None,
) -> AsyncServerProvider:
    from .server import AsyncServer

    if setting is None:
        setting = Setting()

    if database is None:
        database = Database(setting=setting)

    if agent_ai is None:
        agent_ai = GeminiAgentAI(setting=setting)

    vehicle_search_handler: VehicleSearchHandler = VehicleSearchHandler(
        database=database
    )

    vehicle_chat_handler: VehicleChatHandler = VehicleChatHandler(agent_ai=agent_ai)

    router: EventRouterProvider = EventRouter(
        handlers={
            RequestEvent.VEHICLE_SEARCH: vehicle_search_handler,
            RequestEvent.VEHICLE_CHAT: vehicle_chat_handler,
        }
    )

    return AsyncServer(setting=setting, router=router)
