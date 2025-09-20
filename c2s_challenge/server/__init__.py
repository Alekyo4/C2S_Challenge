from c2s_challenge.common.protocol.request import RequestEvent

from c2s_challenge.common.setting import Setting, SettingProvider

from .event import EventRouterProvider, EventRouter

from .event.handler import VehicleSearchHandler

from .database import DatabaseRepository, DatabaseProvider, Database

from .database.repository import VehicleRepository

from .abstract import AsyncServerProvider, SyncServerProvider

def make_server(database: DatabaseProvider | None = None, setting: SettingProvider | None = None) -> SyncServerProvider:
  """Factory function to create a Server instance."""
  raise NotImplementedError()

def make_server_async(database: DatabaseProvider | None = None, setting: SettingProvider | None = None) -> AsyncServerProvider:
  """Factory function to create a AsyncServer instance."""
  from .server import AsyncServer

  if setting is None:
    setting = Setting()

  if database is None:
    database = Database(setting=setting)

  vehicle_repository: DatabaseRepository = VehicleRepository(database=database)
  
  vehicle_search_handler: VehicleSearchHandler = VehicleSearchHandler(
    repository=vehicle_repository)
  
  router: EventRouterProvider = EventRouter(handlers={
    RequestEvent.VEHICLE_SEARCH: vehicle_search_handler
  })

  return AsyncServer(setting, router)