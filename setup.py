from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="secxbrl",
    version="0.0.7",
    description="A package to parse SEC XBRL",
    packages=find_packages(),
    install_requires=['selectolax'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT"
)