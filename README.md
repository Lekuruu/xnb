# XNB

A python tool for reading xnb files.

At this point it can only deserialize `Texture2DReader` files with the BGRA surface format, but the project should allow for extension of the reader classes. I mostly used [this code](https://github.com/MonoGame/MonoGame/blob/develop/MonoGame.Framework/Content/ContentReaders/Texture2DReader.cs) as a reference for it.

## Installation & Usage

```sh
python -m pip install git+https://github.com/Lekuruu/xnb.git
```

### Using the cli

```sh
python -m xnb <INPUT> <OUTPUT>
```

### Usage of the reader class

```python
from xnb import XNBReader
import logging

# Initialize the class from a filepath
reader = XNBReader.from_file('./your_file.xnb')

# Initialize the class from bytes
reader = XNBReader(b'...')

# When initializing the class, it will already try
# to automatically deserialize the file. You can
# turn on logging to view the process in detail.
logging.basicConfig(level=logging.INFO)

# Access the deserialized content
data = reader.content

# Save the xnb data into a readable file
reader.save('./your_output.png')
```