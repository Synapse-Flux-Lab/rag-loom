# setup.py
from setuptools import setup, find_packages

setup(
    name="rag-platform-kit",
    version="0.1.0",
    packages=find_packages(include=["app*"]),
    package_dir={"": "."},
)
