
from __future__ import annotations
from typing import Any, List

from .streams import StreamIn
from .readers import *

import logging

class XNBReader:
    """A class to read the xnb format"""

    Readers = {
        'Microsoft.Xna.Framework.Content.Texture2DReader': Texture2DReader
        # TODO: Add more readers...
    }

    SupportedVersions = (
        1, 2, 4, 5
    )

    def __init__(self, data: bytes) -> None:
        self.stream = StreamIn(data)
        self.logger = logging.getLogger(__name__)
        self.readers: List[BaseReader] = []
        self.platform = 'w'
        self.version = 1
        self.flags = 0
        self.deserialize()

    @classmethod
    def from_file(cls, filepath: str) -> "XNBReader":
        """Initialize the reader from a file path"""
        with open(filepath, 'rb') as f:
            return cls(f.read())

    @property
    def contents(self) -> List[Any]:
        return [
            reader.content for reader in self.readers
        ]

    def save(self, path: str) -> None:
        """Save the xnb data into readable file(s)"""
        if not self.readers:
            self.logger.error('No readers were found.')
            return

        for reader in self.readers:
            reader.content.save(path)

    def deserialize(self) -> None:
        """Deserialize the xnb file"""
        self.validate_header()

        if self.readers:
            # Texture reader was forced
            return

        reader_classes = self.read_content_manifest()

        for reader in reader_classes:
            reader_index = self.stream.uleb128()

            assert reader_index > 0, 'Invalid reader index'
            assert reader_index <= len(reader_classes), 'Invalid reader index'

            self.readers.append(reader(self.stream))

    def validate_header(self) -> None:
        header = self.stream.read(3)

        if not header.startswith(b'XNB'):
            # Try to skip the header
            self.force_texture_reader()
            return

        self.platform = self.stream.char()
        self.version = self.stream.u8()
        self.flags = self.stream.u8()

        assert self.version in self.SupportedVersions, 'Invalid xnb version'

        lzx_compressed = self.flags & 0x80
        lz4_compressed = self.flags & 0x40

        # TODO: Implement compression methods
        assert not any([lzx_compressed, lz4_compressed]), 'Unsupported compression method'

        # We just ignore this and continue using the stream
        xnb_size = self.stream.s32()

    def read_content_manifest(self) -> List[BaseReader]:
        # Each xnb file can contain multiple readers
        reader_amount = self.stream.uleb128()
        reader_classes = [None]*reader_amount

        assert reader_amount > 0, 'No readers found'

        for index in range(reader_amount):
            reader_class = self.stream.string()
            version = self.stream.s32()

            reader = self.Readers.get(reader_class)
            assert reader is not None, f'Unsupported content reader: "{reader_class}"'

            if reader.Version != version:
                # The version seems to be always set to 0, but we'll keep this here just in case
                self.logger.warning(f'Unsupported reader version "{version}", continuing anyways...')

            reader_classes[index] = reader

        # TODO: Implement shared resource fixups
        shared_resource_fixups = self.stream.uleb128()
        assert shared_resource_fixups == 0, 'Shared resource fixups are not supported'

        return reader_classes

    def force_texture_reader(self) -> None:
        # In some cases, the header is not present, so
        # we just assume its a Texture2DReader and
        # skip the header part.
        # This is a very hacky workaround, but it's
        # required for some files.

        self.stream.skip(10) # Skip header
        self.readers = [Texture2DReader(self.stream)]
