from google.generativeai import GenerativeModel, configure as genai_configure

from google.generativeai.types import AsyncGenerateContentResponse

from c2s_challenge.common.setting import SettingProvider

from c2s_challenge.common.protocol.dto import ChatMessageDto

from .abstract import AgentAIProvider

class GeminiAgentAI(AgentAIProvider):
  model: GenerativeModel

  def __init__(self, setting: SettingProvider):
    super().__init__(setting)

    genai_configure(api_key=setting.get_required("GEMINI_API_KEY"))

    self.model = GenerativeModel(
      model_name="gemini-1.5-flash",
      system_instruction=self.system_prompt
    )

  async def ask_llm(self, history: list[ChatMessageDto], tools: list[dict] | None = None) -> None:
    genai_history: list[dict[str, str]] = [
      { "role": "model" if msg.role == "assistant" else "user", "content": msg.content } for msg in history 
    ]

    response: AsyncGenerateContentResponse = await self.model.generate_content_async(genai_history, tools=tools)

    res_part: any = response.candidates[0].content.parts[0]

    print(response, res_part)