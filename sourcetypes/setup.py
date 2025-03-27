from setuptools import setup
from pathlib import Path
README=Path(__file__).parent.parent.joinpath("README.md")

with open(README, "r") as fh:
    long_description = fh.read()

setup(
    name='sourcetypes3',
    version='0.0.6',
    author="Aurin Aegerter",
    description="Python Source Code Types For Inline Syntax Highlighting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrxer/python-inline-source-3",
    packages=['sourcetypes'],
    package_data={'sourcetypes': ['py.typed']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'typing-extensions>=3.7.4',
    ]
)
