# setup.py
from setuptools import setup, find_packages

setup(
    name="rag-loom",
    version="0.2.0",
    packages=find_packages(include=["app*"]),
    package_dir={"": "."},
)
