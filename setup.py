#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# I really prefer Markdown to reStructuredText. PyPi does not. This allows me
# to have things how I'd like, but not throw complaints when people are trying
# to install the package and they don't have pypandoc or the README in the
# right place.
try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

about = {}
with open('src/clikraken/__about__.py') as f:
    exec(f.read(), about)
# now we have a about['__version__'] variable

with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

setup(
    name=about['__title__'],
    version=about['__version__'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[req for req in requirements if req[:2] != "# "],
    author=about['__author__'],
    author_email=about['__email__'],
    license=about['__license__'],
    description=about['__summary__'],
    long_description=long_description,
    include_package_data=True,
    url=about['__url__'],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    entry_points={
        'console_scripts': [
            'clikraken=clikraken.clikraken:main',
        ],
    },
)
