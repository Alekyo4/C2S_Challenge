from pydantic import BaseModel

from typing import Optional, Dict, Any

class LLMResponse(BaseModel):
  is_tool_call: bool = False

  tool_name: Optional[str] = None

  tool_arguments: Optional[Dict[str, Any]] = None

  text: Optional[str] = None