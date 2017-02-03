import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="Pushy",
    version="0.1.0",
    author="Rob Kent",
    author_email="jazzycamel@googlemail.com",
    description=("A very simple Python client for the Pushy notification service API.",),
    license="MIT",
    keywords="Pushy Notification API",
    url="https://github.com/jazzycamel/pushy",
    packages=find_packages(exclude=['docs','tests']),
    install_requires=['requests','six'],
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
    ]
)