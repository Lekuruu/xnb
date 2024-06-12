
import setuptools
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(current_directory, "README.md"), "r") as f:
    long_description = f.read()

with open(os.path.join(current_directory, "requirements.txt"), "r") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="xnb",
    version="1.0.0",
    author="Lekuru",
    author_email="contact@lekuru.xyz",
    description="Python utils for the xnb file format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    keywords=["xnb", "xna", "xna-framework", "python"],
)
