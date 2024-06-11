# XNB

A python tool for reading xnb files.

Don't expect everything to work, this was a small attempt at decompiling and re-implementing this format. It supports both the old and new xnb format, but can only convert BGRA textures at the moment. I mostly used [this code](https://github.com/MonoGame/MonoGame/blob/develop/MonoGame.Framework/Content/ContentReaders/Texture2DReader.cs) as a reference for it.