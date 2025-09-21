from c2s_challenge.common.protocol.model import RequestEvent

from c2s_challenge.common.setting import Setting, SettingProvider

from .event import EventRouterProvider, EventRouter

from .event.handler import VehicleSearchHandler, VehicleChatHandler

from .agent import AgentAIProvider, GeminiAgentAI

from .database import DatabaseRepository, DatabaseProvider, Database

from .database.repository import VehicleRepository

from .abstract import AsyncServerProvider, SyncServerProvider

def make_server_sync(
    setting: SettingProvider | None = None,
    database: DatabaseProvider | None = None,
    agent_ai: AgentAIProvider | None = None) -> SyncServerProvider:
  """Factory function to create a SyncServer instance."""
  raise NotImplementedError()

def make_server_async(
    setting: SettingProvider | None = None,
    database: DatabaseProvider | None = None,
    agent_ai: AgentAIProvider | None = None) -> AsyncServerProvider:
  """Factory function to create a AsyncServer instance."""
  from .server import AsyncServer

  if setting is None:
    setting = Setting()

  if database is None:
    database = Database(setting=setting)

  if agent_ai is None:
    agent_ai = GeminiAgentAI(setting=setting)
  
  vehicle_repository: DatabaseRepository = VehicleRepository(database=database)
  
  vehicle_search_handler: VehicleSearchHandler = VehicleSearchHandler(
    repository=vehicle_repository)
  
  vehicle_chat_handler: VehicleChatHandler = VehicleChatHandler(agent_ai=agent_ai)
  
  router: EventRouterProvider = EventRouter(handlers={
    RequestEvent.VEHICLE_SEARCH: vehicle_search_handler,
    RequestEvent.VEHICLE_CHAT:  vehicle_chat_handler
  })

  return AsyncServer(setting=setting, router=router)