from dataclasses import dataclass

@dataclass
class LLMModelConfig:
    name: str
    provider: str
    model: str