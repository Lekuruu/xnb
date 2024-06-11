
from __future__ import annotations

from streams import StreamIn
from typing import List
from PIL import Image

import logging
import numpy
import io

class XNBReader:
    """A class to read the xnb format"""

    def __init__(self, filepath: str) -> None:
        self.width: int | None = None
        self.height: int | None = None
        self.surface_format: int | None = None
        self.using_old_format = False
        self.textures: List[bytes] = []
        self.header = bytes()
        self.stream = StreamIn.from_file(filepath)
        self.logger = logging.getLogger(__name__)
        self.deserialize()

    def deserialize(self) -> None:
        """Deserialize the xnb file"""
        header = self.stream.read(3)
        self.stream.pos = 0

        if not header.startswith(b'XNB'):
            # Read old format
            self.using_old_format = True
            self.header = self.stream.read(13)
            self.surface_format = self.stream.s32()
            self.width = self.stream.s32()
            self.height = self.stream.s32()
            self.level_num = self.stream.s32()
            self.textures.append(self.stream.read(self.stream.u16()))
            return

        # Read new format
        self.stream.skip(10)
        num_sprites = self.stream.uleb128()

        # Skip texture information
        for _ in range(num_sprites):
            self.stream.string()
            self.stream.skip(4)

        self.stream.uleb128()
        self.stream.uleb128()

        # Read texture format, width, height, and number of textures
        self.surface_format = self.stream.s32()
        self.width = self.stream.s32()
        self.height = self.stream.s32()
        num_sprites = self.stream.s32()

        # Create an array to store the textures
        self.image_data = bytes()
        sprites = []

        # Read sprites
        for _ in range(num_sprites):
            sprite_size = self.stream.u32()
            spite_data = self.stream.read(sprite_size)
            sprites.append(spite_data)

        self.textures.extend(sprites)

    def get_images(self, format: str = 'png') -> List[bytes]:
        """Convert the raw image(s) into a readable image format"""
        if not self.textures:
            self.logger.warning('Texture data is empty!')
            return list()

        return [
            self.texture_to_image(texture, format)
            for index, texture in enumerate(self.textures)
        ]

    def save(self, outpath: str, format: str = 'png') -> None:
        """Save the image data into a readable file"""
        images = self.get_images()

        if len(images) <= 0:
            self.logger.warning('No images were parsed!')
            return

        for index, image in enumerate(images):
            path = f'{outpath}-{index}.{format.lower()}'
            with open(path, 'wb') as f:
                f.write(image)

    def texture_to_image(self, texture: bytes, format: str = 'png') -> bytes:
        bitmap = numpy.frombuffer(texture, dtype=numpy.uint8).copy()

        if len(bitmap) <= 0:
            return bytes()

        bitmap = self.convert_brga_to_rgba(bitmap)
        width = self.width
        height = self.height

        if self.using_old_format:
            # Calculate width and height with each pixel having 4 bytes (RGBA)
            pixel_count = len(bitmap) // 4
            width = int(pixel_count ** 0.5)
            height = pixel_count // width

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

    def convert_brga_to_rgba(self, bitmap: numpy.ndarray) -> numpy.ndarray:
        """Convert BGRA to RGBA"""
        if self.surface_format != 1:
            self.logger.warning(f'Texture format is not BGRA. ({self.surface_format})')
            return bitmap

        for i in range(0, len(bitmap), 4):
            b0 = bitmap[i]

            bitmap[i] = bitmap[i + 2]
            bitmap[i + 2] = b0

        return bitmap
