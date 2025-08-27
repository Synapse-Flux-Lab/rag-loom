from setuptools import setup, find_packages

setup(
    name="app",
    version="0.1.0",
    packages=find_packages(where='.', include=['app', 'app.*'])
    package_dir={"": "."},
)
