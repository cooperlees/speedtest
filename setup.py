#!/usr/bin/env python3

# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from pathlib import Path
from setuptools import setup


def get_long_desc() -> str:
    repo_base = Path(__file__).parent
    info_file = repo_base / "README.md"
    with info_file.open("r", encoding="utf8") as ifp:
        long_desc = ifp.read()

    return long_desc


setup(
    name="speedtest_wrapper",
    version="22.9.21",
    description="Wrap the speedtest cli and exports stats for prometheus",
    long_description=get_long_desc(),
    long_description_content_type="text/markdown",
    py_modules=["speedtest_wrapper"],
    url="http://github.com/cooperlees/speedtest",
    author="Cooper Lees",
    author_email="me@cooperlees.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    entry_points={"console_scripts": ["speedtest-wrapper = speedtest_wrapper:main"]},
    install_requires=["prometheus_client"],
)
