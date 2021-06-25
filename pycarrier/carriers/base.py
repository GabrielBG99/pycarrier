from abc import ABC, abstractmethod
from ..event import Event


class BaseCarreier(ABC):
    @abstractmethod
    async def track(self, code: str) -> list[Event]:
        raise NotImplementedError
