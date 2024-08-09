
from __future__ import annotations

from ..constants import SurfaceFormat
from ..objects import Texture2D
from ..streams import StreamIn
from .Base import BaseReader

class Texture2DReader(BaseReader):
    def __init__(self, stream: StreamIn) -> None:
        self.texture: Texture2D | None = Texture2D()
        super().__init__(stream)

    def deserialize(self) -> Texture2D:
        # Read texture format, width, height, and number of textures
        self.texture.surface_format = SurfaceFormat(self.stream.s32())
        self.texture.width = self.stream.s32()
        self.texture.height = self.stream.s32()
        level_count = self.stream.s32()

        # Read sprites
        for _ in range(level_count):
            sprite_size = self.stream.u32()
            spite_data = self.stream.read(sprite_size)
            self.texture.textures.append(spite_data)

        return self.texture