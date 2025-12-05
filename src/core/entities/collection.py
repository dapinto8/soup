from dataclasses import dataclass
from uuid import UUID

@dataclass
class Collection:
    id: UUID
    name: str
    metadata: dict