from setuptools import find_packages, setup

from nlogging import __version__

with open("README.md") as f:
    long_description = f.read()

setup(
    name="nlogging",
    version=__version__,
    description=(
        "A tiny logging tool for Python, heavily opinionated, but very easy to use."
    ),
    package_dir={"": "nlogging"},
    packages=find_packages(where="nlogging"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/firminoneto11/nlogging",
    author="Firmino Neto",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.12",
    ],
    # install_requires=[],
    extras_require={"dev": ["pytest>=7.4.3", "ruff>=0.1.8", "twine>=4.0.2"]},
    python_requires=">=3.9",
)
