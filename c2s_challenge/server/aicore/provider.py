from abc import ABC, abstractmethod

from pydantic import BaseModel

from c2s_challenge.common.protocol.dto import ChatMessageDto

from .contracts import LLMResponse


class LLMProvider(ABC):
    system_prompt: str

    api_key: str

    @abstractmethod
    def __init__(self, api_key: str, system_prompt: str):
        self.api_key = api_key

        self.system_prompt = system_prompt

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
