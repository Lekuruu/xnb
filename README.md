# XNB

A python tool for reading xnb files.

At this point it can only deserialize `Texture2DReader` files with the BGRA surface format, but the project should allow for extension of the reader classes. I mostly used [this code](https://github.com/MonoGame/MonoGame/blob/develop/MonoGame.Framework/Content/ContentReaders/Texture2DReader.cs) as a reference for it.