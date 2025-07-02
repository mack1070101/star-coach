#!/usr/bin/env python3
"""
Setup script for STAR Coach CLI tool.
"""

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="star-coach",
    version="0.1.0",
    author="STAR Coach Team",
    author_email="team@starcoach.dev",
    description="A CLI tool for practicing STAR interview answers with timed sections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mack1070101/star-coach",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "star-coach=star_coach.cli:app",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 