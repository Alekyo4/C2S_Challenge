from json import loads as json_loads

from google.ai.generativelanguage_v1beta import Part
from google.generativeai import GenerativeModel
from google.generativeai import configure as genai_configure
from google.generativeai.types import (
    AsyncGenerateContentResponse,
    ContentsType,
    GenerationConfigType,
)
from pydantic import BaseModel

from c2s_challenge.common.protocol.dto import ChatMessageDto

from .contracts import LLMResponse
from .provider import LLMProvider


class GeminiLLM(LLMProvider):
    model: GenerativeModel

    def __init__(self, api_key: str, system_prompt):
        super().__init__(api_key, system_prompt)

        genai_configure(api_key=self.api_key)

        self.model = GenerativeModel(
            model_name="gemini-2.5-flash-lite", system_instruction=self.system_prompt
        )

    def __to_genai_history(self, history: list[ChatMessageDto]) -> ContentsType:
        return [
            {
                "role": "model" if msg.role == "assistant" else "user",
                "parts": [{"text": msg.content}],
            }
            for msg in history
        ]

    async def get_chat_response(
        self, history: list[ChatMessageDto], tools: list[dict[str, any]] | None = None
    ) -> LLMResponse:
        response: AsyncGenerateContentResponse = (
            await self.model.generate_content_async(
                contents=self.__to_genai_history(history), tools=tools
            )
        )

        res_part: Part = response.candidates[0].content.parts[0]

        if not res_part.function_call:
            return LLMResponse(text=res_part.text)

        args_dict = {key: value for key, value in res_part.function_call.args.items()}

        return LLMResponse(
            is_tool_call=True,
            tool_name=res_part.function_call.name,
            tool_arguments=args_dict,
        )

    async def extract_structured(
        self, history: list[ChatMessageDto], schema: type[BaseModel]
    ) -> LLMResponse:
        genai_config: GenerationConfigType = {
            "response_mime_type": "application/json",
            "response_schema": schema,
        }

        response: AsyncGenerateContentResponse = (
            await self.model.generate_content_async(
                contents=self.__to_genai_history(history),
                generation_config=genai_config,
            )
        )

        res_model: dict[str, any] = json_loads(response.text)

        res_model = {field: res_model.get(field, None) for field in schema.model_fields}

        validate: BaseModel = schema.model_construct(**res_model)

        return LLMResponse(tool_arguments=validate, is_tool_call=True)
