
from __future__ import annotations
from typing import List
from PIL import Image

from ..constants import SurfaceFormat
from ..streams import StreamIn
from .Base import BaseReader

import logging
import numpy
import io

class Texture2DReader(BaseReader):
    def __init__(self, stream: StreamIn) -> None:
        self.width: int | None = None
        self.height: int | None = None
        self.surface_format: SurfaceFormat | None = None
        self.textures: List[bytes] = []
        self.image_data: bytes = bytes()
        self.logger = logging.getLogger(__name__)
        super().__init__(stream)

    @property
    def content(self) -> List[bytes]:
        return self.images()

    def deserialize(self) -> None:
        # Read texture format, width, height, and number of textures
        self.surface_format = SurfaceFormat(self.stream.s32())
        self.width = self.stream.s32()
        self.height = self.stream.s32()
        level_count = self.stream.s32()

        # Read sprites
        for _ in range(level_count):
            sprite_size = self.stream.u32()
            spite_data = self.stream.read(sprite_size)
            self.textures.append(spite_data)

    def save(self, path: str, format: str = 'png') -> None:
        """Save the image data into a readable file"""
        if len(self.content) <= 0:
            self.logger.info('No images were parsed.')
            return

        for index, image in enumerate(self.content):
            with open(f'{path}-{index}.{format.lower()}', 'wb') as f:
                f.write(image)

    def images(self, format: str = 'png') -> List[bytes]:
        """Convert the raw image(s) into a readable image format"""
        if not self.textures:
            self.logger.info('Texture data is empty.')
            return list()

        return [
            self.texture_to_image(texture, format, index)
            for index, texture in enumerate(self.textures)
        ]

    def texture_to_image(self, texture: bytes, format: str = 'png', level: int = 0) -> bytes:
        bitmap = numpy.frombuffer(texture, dtype=numpy.uint8).copy()

        if len(bitmap) <= 0:
            return bytes()

        bitmap = self.convert_texture_to_rgba(bitmap)
        width = self.width >> level
        height = self.height >> level

        try:
            # Reshape the flattened array to 3D (height, width, channels)
            image_data = bitmap.reshape((height, width, 4))
        except ValueError as e:
            self.logger.warning(f'Failed to reshape image: {e}')
            return bytes()

        output = io.BytesIO()
        image = Image.fromarray(image_data.astype('uint8'))
        image.save(output, format)
        return output.getvalue()

    def convert_texture_to_rgba(self, bitmap: numpy.ndarray) -> numpy.ndarray:
        """Convert the given surface format to RGBA"""
        format_converters = {
            SurfaceFormat.Bgr565: self.convert_bgra_to_rgba
            # TODO: Add more converters...
        }

        if not (format := format_converters.get(self.surface_format)):
            self.logger.warning(f'Unsupported surface format: {self.surface_format}')
            return bitmap

        return format(bitmap)

    @staticmethod
    def convert_bgra_to_rgba(bitmap: numpy.ndarray) -> numpy.ndarray:
        """Convert BGRA to RGBA"""
        for i in range(0, len(bitmap), 4):
            b0 = bitmap[i]

            bitmap[i] = bitmap[i + 2]
            bitmap[i + 2] = b0

        return bitmap
