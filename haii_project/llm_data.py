from dataclasses import dataclass, asdict
from typing import List

@dataclass()
class llm_data:
    context: str
    max_tokens: int
    temperature: float
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    repeat_penalty: float
    top_k: int
    stop: List[str]
