from dataclasses import dataclass

@dataclass
class LLMModelConfig:
    provider: str
    model: str