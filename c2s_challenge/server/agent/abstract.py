from abc import ABC, abstractmethod

from c2s_challenge.common.protocol.dto import ChatMessageDto

from c2s_challenge.common.setting import SettingProvider

class AgentAIProvider(ABC):
  system_prompt: str

  def __init__(self, setting: SettingProvider):
    self.system_prompt = setting.get_required("AGENT_SYSTEM_PROMPT")

  @abstractmethod
  async def ask_llm(self, history: list[ChatMessageDto], tools: list[dict] | None = None) -> None:
    raise NotImplementedError()