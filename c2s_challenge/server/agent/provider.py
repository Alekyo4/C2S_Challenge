from abc import ABC, abstractmethod

from pydantic import BaseModel

from c2s_challenge.common.protocol.dto import ChatMessageDto
from c2s_challenge.common.setting import SettingProvider

from .model import LLMResponse


class AgentAIProvider(ABC):
    system_prompt: str

    def __init__(self, setting: SettingProvider):
        self.system_prompt = setting.get_required("AGENT_SYSTEM_PROMPT")

    @abstractmethod
    async def get_chat_response(
        self, history: list[ChatMessageDto], tools: list[dict[str, any]] | None = None
    ) -> LLMResponse:
        raise NotImplementedError()

    @abstractmethod
    async def extract_structured(
        self, history: list[ChatMessageDto], schema: type[BaseModel]
    ) -> LLMResponse:
        raise NotImplementedError()
