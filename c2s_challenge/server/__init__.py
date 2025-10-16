from c2s_challenge.common.protocol.model import RequestEvent
from c2s_challenge.common.setting import Setting, SettingProvider

from .aicore import GeminiLLM, LLMProvider
from .database import Database, DatabaseProvider
from .event import EventRouter, EventRouterProvider
from .event.handler import VehicleChatHandler, VehicleSearchHandler
from .provider import AsyncServerProvider, SyncServerProvider


def make_server_router(
    setting: SettingProvider, database: DatabaseProvider
) -> EventRouterProvider:
    vehicle_llm: LLMProvider = GeminiLLM(
        api_key=setting.get_required("GEMINI_API_KEY"),
        system_prompt=setting.get_required("VEHICLE_SYSTEM_PROMPT"),
    )

    vehicle_search_handler: VehicleSearchHandler = VehicleSearchHandler(
        database=database
    )

    vehicle_chat_handler: VehicleChatHandler = VehicleChatHandler(llm=vehicle_llm)

    return EventRouter(
        handlers={
            RequestEvent.VEHICLE_SEARCH: vehicle_search_handler,
            RequestEvent.VEHICLE_CHAT: vehicle_chat_handler,
        }
    )


def make_server_sync(
    setting: SettingProvider | None = None,
    database: DatabaseProvider | None = None,
    router: EventRouterProvider | None = None,
) -> SyncServerProvider:
    raise NotImplementedError()


def make_server_async(
    setting: SettingProvider | None = None,
    database: DatabaseProvider | None = None,
    router: EventRouterProvider | None = None,
) -> AsyncServerProvider:
    from .server import AsyncServer

    if setting is None:
        setting = Setting()

    if database is None:
        database = Database(setting=setting)

    if router is None:
        router = make_server_router(setting=setting, database=database)

    return AsyncServer(setting=setting, router=router)
