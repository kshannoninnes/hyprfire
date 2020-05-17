#!/usr/bin/env python
from setuptools import setup, find_packages, os

setup(
    name='hyprfire',
    version='1.0',
    packages=find_packages(),
    scripts=['manage.py'],
    license='---',
    author='Curtin Capstone 2020 - Group 23 (Stefan Cyber)',
    description='A web app tool hosted on localhost server to help analyse pcap data for anomalous events.',
    install_requires=[
        "hyprfire",
        "asgiref>=3.2.7",
        "asgiref>=3.2.7",
        "Django==3.0.5",
        "plotly>=4.6.0",
        "pytz>=2019.3",
        "retrying>=1.3.3",
        "six>=1.14.0",
        "sqlparse>=0.3.1",
        "scapy>=2.4.3.dev549",
        # "wireshark>=2.6.10",
    ],
    include_package_data=True,
)
# oldmask = os.umask(000)
# os.makedirs('logs', exist_ok=True, mode=0o775)
# os.makedirs('pcaps', exist_ok=True, mode=0o775)
# os.umask(oldmask)
