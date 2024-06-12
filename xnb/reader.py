
from __future__ import annotations
from typing import Any

from .streams import StreamIn
from .readers import *

import logging

class XNBReader:
    """A class to read the xnb format"""

    Readers = {
        'Microsoft.Xna.Framework.Content.Texture2DReader': Texture2DReader
        # TODO: Add more readers...
    }

    def __init__(self, data: bytes) -> None:
        self.stream = StreamIn(data)
        self.logger = logging.getLogger(__name__)
        self.reader: BaseReader | None = None
        self.deserialize()

    @classmethod
    def from_file(cls, filepath: str) -> "XNBReader":
        """Initialize the reader from a file path"""
        with open(filepath, 'rb') as f:
            return cls(f.read())

    @property
    def content(self) -> Any:
        return (
            self.reader.content
            if self.reader else None
        )

    def deserialize(self) -> None:
        """Deserialize the xnb file"""
        header = self.stream.read(3)
        self.stream.pos = 0

        if not header.startswith(b'XNB'):
            # Try to skip the header
            self.force_texture_reader()
            return

        # TODO: Additional header validation
        self.stream.skip(10)

        reader_amount = self.stream.uleb128()
        reader_class = None

        if reader_amount > 1:
            # TODO: I have yet to figure out how to handle this case
            self.logger.warning(f'Multiple content readers found, continuing...')

        for _ in range(reader_amount):
            content_reader = self.stream.string()
            version = self.stream.s32()

            if not (reader := self.Readers.get(content_reader)):
                self.logger.warning(f'Unsupported content reader: "{content_reader}"')
                continue

            if reader.Version != version:
                # The version seems to be always set to 0, but we'll keep this here just in case
                self.logger.warning(f'Unsupported reader version "{version}", continuing...')

            reader_class = reader

        if not reader_class:
            return

        self.stream.uleb128() # TODO
        self.stream.uleb128() # TODO

        self.reader = reader_class(self.stream)

    def save(self, path: str) -> None:
        """Save the xnb data into a readable file"""
        if not self.reader:
            self.logger.error('No reader was found.')
            return

        self.reader.save(path)

    def force_texture_reader(self) -> None:
        # In some cases, the header is not present, so
        # we just assume its a Texture2DReader and
        # skip the header part.
        # This is a very hacky workaround, but it's
        # required for some files.

        try:
            self.stream.skip(13) # Skip header
            self.reader = Texture2DReader(self.stream)
        except Exception as e:
            self.logger.error('Invalid XNB file')
            self.reader = None
