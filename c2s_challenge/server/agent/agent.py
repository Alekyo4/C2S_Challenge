from google.generativeai import GenerativeModel, configure as genai_configure

from google.generativeai.types import (
    AsyncGenerateContentResponse,
    GenerationConfigType,
    ContentsType,
)

from google.ai.generativelanguage_v1beta import Part

from pydantic import BaseModel

from c2s_challenge.common.setting import SettingProvider

from c2s_challenge.common.protocol.dto import ChatMessageDto

from .model import LLMResponse

from .abstract import AgentAIProvider


class GeminiAgentAI(AgentAIProvider):
    model: GenerativeModel

    def __init__(self, setting: SettingProvider):
        super().__init__(setting)

        genai_configure(api_key=setting.get_required("GEMINI_API_KEY"))

        self.model = GenerativeModel(
            model_name="gemini-1.5-flash", system_instruction=self.system_prompt
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

        validate: BaseModel = schema.model_validate_json(response.text)

        return LLMResponse(
            tool_arguments=validate.model_dump(exclude_none=True), is_tool_call=True
        )
