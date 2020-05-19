#!/usr/bin/env python
from setuptools import setup, find_packages, os

setup(
    name='hyprfire',
    version='1.0',
    packages=find_packages(),
    scripts=['manage.py'],
    author='Curtin Capstone 2020 - Group 23 (Stefan Cyber)',
    description='A web app tool hosted on localhost server to help analyse pcap data for anomalous events.',
    install_requires=[],
    include_package_data=True,
)
os.makedirs('logs', exist_ok=True)
os.makedirs('pcaps', exist_ok=True)
