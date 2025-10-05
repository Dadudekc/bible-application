#!/usr/bin/env python3
"""
Bible Mathematical Discovery Suite
Setup script for package installation
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="bible-mathematical-discovery",
    version="1.0.0",
    author="Bible Mathematical Discovery Suite",
    author_email="research@biblemath.org",
    description="Scientific proof of divine authorship through Hebrew Gematria analysis",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bible-mathematical-discovery",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
        "analysis": [
            "numpy>=1.20.0",
            "scipy>=1.6.0",
            "matplotlib>=3.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bible-analyzer=full_bible_analyzer:main",
            "bible-downloader=clean_bible_downloader:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.html", "*.css", "*.js", "*.json", "*.md"],
    },
    keywords="bible, gematria, hebrew, mathematics, statistics, analysis, tanakh, torah",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/bible-mathematical-discovery/issues",
        "Source": "https://github.com/yourusername/bible-mathematical-discovery",
        "Documentation": "https://github.com/yourusername/bible-mathematical-discovery/wiki",
    },
)

