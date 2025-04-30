#!/usr/bin/env python3
"""
Setup script for Random Log Generator.
"""

from setuptools import setup, find_packages

# Read version from package __init__.py
with open('random_log_generator/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip("'").strip('"')
            break
    else:
        version = '0.0.1'

# Read long description from README.md
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='random-log-generator',
    version=version,
    description='Generate realistic log entries with configurable rates and formats',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='sd416',
    url='https://github.com/sd416/random-log-generator',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyyaml>=6.0',
    ],
    entry_points={
        'console_scripts': [
            'random-log-generator=random_log_generator.cli:main',
        ],
    },
    classifiers=[
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: System :: Logging',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    python_requires='>=3.9',
)