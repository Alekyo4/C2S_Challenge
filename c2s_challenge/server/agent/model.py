from typing import Any, Dict, Optional

from pydantic import BaseModel


class LLMResponse(BaseModel):
    is_tool_call: bool = False

    tool_name: Optional[str] = None

    tool_arguments: Optional[Dict[str, Any]] = None

    text: Optional[str] = None
