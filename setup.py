"""Python setup.py for sandbox_exporter package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("sandbox_exporter", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="sandbox_exporter",
    version=read("sandbox_exporter", "VERSION"),
    description="Awesome sandbox_exporter created by bkm82",
    url="https://github.com/bkm82/sandbox_exporter/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="bkm82",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["sandbox_exporter = sandbox_exporter.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
