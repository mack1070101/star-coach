#!/usr/bin/env python3
"""
Setup script for STAR Coach
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="star-coach",
    version="2.1.0",
    author="Mackenzie Bligh",
    author_email="mackenziebligh@gmail.com",
    description="STAR Coach - Interview timer for managing your STAR answers with timed sections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mack1070101/star-coach",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "star-coach=star_coach.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "star_coach": ["*.org", "*.txt"],
    },
    keywords="interview, star, timer, cli, practice",
    project_urls={
        "Homepage": "https://github.com/mack1070101/star-coach",
        "Repository": "https://github.com/mack1070101/star-coach",
        "Issues": "https://github.com/mack1070101/star-coach/issues",
    },
) 