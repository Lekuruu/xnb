
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from PIL import Image

from ..constants import SurfaceFormat

import logging
import numpy
import io

@dataclass
class Texture2D:
    width: int = 0
    height: int = 0
    surface_format: SurfaceFormat = SurfaceFormat.Bgr565
    textures: List[bytes] = field(default_factory=list)
    image_data: bytes = bytes()
    logger: logging.Logger = logging.getLogger(__name__)

    def save(self, path: str, format: str = 'png') -> None:
        """Save the image data into a readable file"""
        images = self.images(format)

        if len(images) <= 0:
            self.logger.info('No images were parsed.')
            return

        for index, image in enumerate(images):
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
            bitmap[i], bitmap[i + 2] = bitmap[i + 2], bitmap[i]

        return bitmap