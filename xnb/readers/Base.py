
from ..streams import StreamIn
from typing import Any

class BaseReader:
    Version = 0

    def __init__(self, stream: StreamIn) -> None:
        self.stream = stream
        self.deserialize()

    @classmethod
    def from_bytes(cls, data: bytes) -> "BaseReader":
        stream = StreamIn(data)
        return cls(stream)

    @property
    def content(self) -> Any:
        """Get the deserialized content"""
        ...

    def deserialize(self) -> None:
        """Deserialize the xnb data"""
        ...

    def save(self, path: str) -> None:
        """Save the xnb data into a readable file"""
        ...
