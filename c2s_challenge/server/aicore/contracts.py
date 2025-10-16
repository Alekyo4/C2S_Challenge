from typing import Optional

from pydantic import BaseModel


class LLMResponse(BaseModel):
    is_tool_call: bool = False

    tool_name: Optional[str] = None

    tool_arguments: Optional[BaseModel] = None

    text: Optional[str] = None
