from setuptools import setup, find_packages
import os
print(os.getcwd())

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="secxbrl",
    version="0.0.2",
    description="A package to parse SEC XBRL",
    packages=find_packages(),
    install_requires=['selectolax'],
    long_description=long_description,
    long_description_content_type="text/markdown",
)