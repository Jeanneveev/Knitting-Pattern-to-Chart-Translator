"""Setup for CLI app package"""

from setuptools import setup, find_packages

setup(
    name="pattern_to_chart",
    version="0.1.0",
    description="A CLI app for the Knitting Pattern Parser project",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pattern_to_chart=src.infrastructure.cli.cli:cli"
        ],
    },
    install_requires=[
        "setuptools"
    ],
    python_requires=">=3.1"
)