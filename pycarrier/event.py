from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any


@dataclass
class Event:
    time: datetime
    local: str
    title: str
    detail: str

    def dict(self) -> dict[str, Any]:
        return asdict(self)
